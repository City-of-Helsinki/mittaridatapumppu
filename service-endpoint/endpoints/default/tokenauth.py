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
        Use Starlette request_data here to determine should we accept or reject this request
        :param request_data: deserialized Starlette Request
        :return: (bool ok, str error text, int status code)
        """
        # Reject requests not matching the one defined in env
        endpoint_path = os.getenv("ENDPOINT_PATH")
        if request_data["path"] not in [endpoint_path]:
            return False, "Not found", 404
        # Reject requests without token parameter, which can be in query string or http header
        api_token = request_data["request"]["get"].get("token")
        if api_token is None:
            api_token = request_data["request"]["headers"].get("x-api-key")
        if api_token is None or api_token != os.getenv("AUTH_TOKEN"):
            logging.warning("Missing or invalid authentication token")
            return (
                False,
                "Missing or invalid authentication token, see logs for error",
                401,
            )
        elif request_data["request"]["get"].get("test") == "true":
            logging.info("Test ok")
            return False, "Test OK", 400
        return True, None, None

    async def process_request(
        self, request_data: dict
    ) -> Tuple[bool, str, Union[str, None], Union[str, dict, list], int]:
        """
        Just do minimal validation for request_data and
        return ok if token was valid.
        """
        auth_ok, response_message, status_code = await self.validate(request_data)
        if auth_ok:
            topic_name = os.getenv("KAFKA_RAW_DATA_TOPIC_NAME")
            response_message = "Request OK"
            status_code = 202
        else:
            topic_name = None
        return auth_ok, "device_id", topic_name, response_message, status_code

    async def get_metadata(self, request_data: dict, device_id: str) -> str:
        metadata = "{}"
        # Get metadata from somewhere here, if needed
        return metadata
