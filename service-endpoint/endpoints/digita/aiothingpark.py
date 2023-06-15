import logging
import os
from typing import Tuple, Union

from endpoints import AsyncRequestHandler


class RequestHandler(AsyncRequestHandler):
    @staticmethod
    async def validate(
        request_data: dict,
    ) -> Tuple[bool, Union[str, None], Union[int, None]]:
        """
        Use Starlette request_data here to determine should we accept or reject
        this request
        :param request_data: deserialized (FastAPI) Starlette Request
        :return: (bool ok, str error text, int status code)
        """
        # Reject requests not matching the one defined in env
        endpoint_path = os.getenv("ENDPOINT_PATH")
        if request_data["path"] not in [endpoint_path]:
            return False, "Not found", 404
        # Reject requests without valid AUTH_TOKEN, which is defined in env
        auth_token = request_data["request"]["get"].get("token")
        if auth_token is None or auth_token != os.getenv("AUTH_TOKEN"):
            logging.warning("Missing or invalid authentication token")
            return False, "Missing or invalid authentication token", 401
        logging.info("Authentication token validated")
        if request_data["request"]["get"].get("test") == "true":
            logging.info("Test ok")
            return False, "Test OK", 400
        allowed_ip_addresses = os.getenv("ALLOWED_IP_ADDRESSES")
        if allowed_ip_addresses is None:
            logging.warning(
                "Set ALLOWED_IP_ADDRESSES to restrict requests unknown sources"
            )
        else:
            # TODO: to a function
            allowed_ips = allowed_ip_addresses.split(",")
            known_ips = [request_data["remote_addr"]]
            known_ips += (
                request_data["request"]["headers"].get("x-forwarded-for", "").split(",")
            )
            ip_allowed = None
            for ip in known_ips:
                if ip in allowed_ips:
                    ip_allowed = ip
                    break
            if ip_allowed is None:
                logging.warning(
                    "Remote IP {} was not in ALLOWED_IP_ADDRESSES".format(
                        request_data["remote_addr"]
                    )
                )
            else:
                logging.info(
                    "Remote IP {} was in ALLOWED_IP_ADDRESSES".format(ip_allowed)
                )
        if request_data["request"]["get"].get("LrnDevEui") is None:
            logging.warning("LrnDevEui not found in request params")
            return False, "Invalid arguments, see logs for error", 400
        else:
            return True, "Request accepted", 202

    async def process_request(
        self, request_data: dict
    ) -> Tuple[bool, str, Union[str, None], Union[str, dict, list], int]:
        auth_ok, response_message, status_code = await self.validate(request_data)
        device_id = request_data["request"]["get"].get("LrnDevEui")
        if device_id:  # a LrnDevEui must be present to send the data to Kafka topic
            topic_name = os.getenv("KAFKA_RAW_DATA_TOPIC_NAME")
        else:
            topic_name = None
        logging.info(
            "Validation: {}, {}, {}".format(auth_ok, response_message, status_code)
        )
        return auth_ok, device_id, topic_name, response_message, status_code

    async def get_metadata(self, request_data: dict, device_id: str) -> str:
        # TODO: put this function to BaseRequestHandler or remove from endpoint
        # (and add to parser)
        metadata = "{}"
        redis_url = os.getenv("REDIS_URL")
        if redis_url is None:
            logging.info("No REDIS_URL defined, querying device metadata failed")
            return metadata
        if device_id is None:
            logging.info("No device_id available, querying device metadata failed")
            return metadata
        if metadata is None:
            return "{}"
        return metadata
