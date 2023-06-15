import importlib
import logging
import os
import pprint

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, PlainTextResponse, JSONResponse
from fastapi.routing import APIRoute
from sentry_asgi import SentryMiddleware

from endpoints import AsyncRequestHandler as RequestHandler
from fvhiot.utils import init_script
from fvhiot.utils.aiokafka import (
    get_aiokafka_producer_by_envs,
    on_send_success,
    on_send_error,
)
from fvhiot.utils.data import data_pack
from fvhiot.utils.http.starlettetools import extract_data_from_starlette_request

HTTP_REQUESTHANDLER = os.getenv("HTTP_REQUESTHANDLER", "endpoints.default.tokenauth")
requesthandler = importlib.import_module(HTTP_REQUESTHANDLER)  # noqa


async def root(_request: Request) -> Response:
    return JSONResponse({"message": "Test ok"})


async def readiness(_request: Request) -> Response:
    return PlainTextResponse("OK")


async def healthz(_request: Request) -> Response:
    return PlainTextResponse("OK")


async def trigger_error(_request: Request) -> Response:
    _ = 1 / 0
    return PlainTextResponse("Shouldn't reach this")


async def api_v1(request: Request) -> Response:
    request_data = await extract_data_from_starlette_request(
        request
    )  # data validation done here
    if request_data["extra"]:
        logging.warning(f"RequestModel contains extra values: {request_data['extra']}")
    if request_data["request"]["extra"]:
        logging.warning(
            f"RequestData contains extra values: {request_data['request']['extra']}"
        )
    path = request_data["path"]
    logging.info(f"Process request using {HTTP_REQUESTHANDLER}")
    (
        auth_ok,
        device_id,
        topic_name,
        response_message,
        status_code,
    ) = await app.requesthandler.process_request(request_data)
    response_message = str(response_message)
    # We assume device data is valid here
    logging.debug(pprint.pformat(request_data))
    if topic_name:
        if app.producer:
            logging.info(f'Sending path "{path}" data to {topic_name}')
            packed_data = data_pack(request_data)
            logging.debug(packed_data[:1000])
            try:
                res = await app.producer.send_and_wait(topic_name, value=packed_data)
                on_send_success(res)
            except Exception as e:
                on_send_error(e)
        else:
            logging.error(
                f'Failed to send "{path}" data to {topic_name}, producer was '
                f'not initialised'
            )
            # Endpoint process has failed and no data was sent to Kafka. This
            # is a fatal error.
            response_message, status_code = "Internal server error", 500
    else:
        logging.info("No action: topic_name is not defined")

    return PlainTextResponse(response_message, status_code=status_code or 200)


async def catch_all(request: Request) -> Response:
    full_path = request.path_params["full_path"]
    return PlainTextResponse("full_path: " + full_path)


async def startup():
    """
    Create KafkaProducer.
    TODO: Test external connections here, e.g. device registry, redis etc. and
    crash if some mandatory
    service is missing.
    """
    global app
    app.producer = await get_aiokafka_producer_by_envs()
    # app.producer = None
    logging.info(
        "Ready to go, listening to endpoint path {}".format(
            os.getenv("ENDPOINT_PATH", "<none>??? WTF")
        )
    )


async def shutdown():
    """
    Close KafkaProducer and other connections.
    """
    global app
    logging.info("Shutdown, close connections")
    if app.producer:
        await app.producer.stop()


routes = [
    APIRoute("/", endpoint=root),
    APIRoute("/readiness", endpoint=readiness, methods=["GET", "HEAD"]),
    APIRoute("/healthz", endpoint=healthz, methods=["GET", "HEAD"]),
    APIRoute("/debug-sentry", endpoint=trigger_error, methods=["GET", "HEAD"]),
    APIRoute(
        os.getenv("ENDPOINT_PATH"),
        endpoint=api_v1,
        methods=["GET", "POST", "PUT", "HEAD"],
    ),
    APIRoute("/{full_path:path}", endpoint=catch_all),
]

init_script()
debug = True if os.getenv("DEBUG") else False
app = FastAPI(debug=debug, routes=routes, on_startup=[startup], on_shutdown=[shutdown])
requesthandler: RequestHandler = requesthandler.RequestHandler()  # noqa
app.requesthandler = requesthandler
app.producer = None
app.add_middleware(SentryMiddleware)
