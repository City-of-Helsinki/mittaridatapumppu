import abc
import os
from typing import Tuple, Union


class BaseRequestHandler(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def process_request(
        self, request_data: dict
    ) -> Tuple[bool, Union[str, None], Union[str, dict, list], int]:
        """
        Validate request and generate response
        :param request_data:
        :return: (
            bool: request was valid or not
            str: kafka topic's name
            str/dict/list: response str or dict
            int: HTTP status code
        )
        """
        auth_ok = True
        topic_name = os.getenv("KAFKA_RAW_DATA_TOPIC_NAME")
        response_message = {"status": "ok"}
        status_code = 200
        return auth_ok, topic_name, response_message, status_code


class AsyncRequestHandler(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    async def process_request(
        self, request_data: dict
    ) -> Tuple[bool, Union[str, None], Union[str, None], Union[str, dict, list], int]:
        """
        Validate request and generate response
        :param request_data:
        :return: (
            bool: request was valid or not
            str: kafka topic's name
            str/dict/list: response str or dict
            int: HTTP status code
        )
        """
        auth_ok = True
        device_id = None
        topic_name = os.getenv("KAFKA_RAW_DATA_TOPIC_NAME")
        response_message = {"status": "ok"}
        status_code = 200
        return auth_ok, device_id, topic_name, response_message, status_code

    @abc.abstractmethod
    async def get_metadata(self, request_data: dict, device_id: str) -> str:
        metadata = "{}"
        # Get metadata from somewhere here, if needed
        return metadata


class DeviceIdGenerator(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_device_id(self) -> str:
        pass
