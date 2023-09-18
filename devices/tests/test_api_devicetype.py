from rest_framework.test import APIClient
import pytest
import logging
from django.contrib.auth.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


site_name = "testserver"


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture(scope="function")
def authenticated_client() -> APIClient:
    """
    Fixture to login a user
    """
    api_client = APIClient()
    username = "test_admin"
    password = "test_password"
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    api_client.force_authenticate(user=user)
    return api_client


def test_api_v1_device_type_unauthenticated(api_client) -> None:
    """
    Test the create device type API endpoint
    :param api_client:
    :return: None
    """
    payload = {
        "name": "type1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }

    response_post = api_client.post("/api/v1/device-types/", data=payload, format="json")
    assert response_post.status_code == 403


@pytest.mark.django_db
def test_api_v1_device_type_post(authenticated_client) -> None:
    """
    Test the create device type API endpoint
    :param api_client:
    :return: None
    """
    payload = {
        "name": "type1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }
    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201

    url = response_post.data["url"]
    url_path = url.split(site_name)[1]
    response_get = api_client.get(url_path)
    logger.info(response_get.data)
    assert response_get.data["name"] == payload["name"]
    assert response_get.data["description"] == payload["description"]
    assert response_get.data["additional_data_json"] is None
    assert response_get.data["processors"] == payload["processors"]
    assert response_get.data["documents"] == payload["documents"]


@pytest.mark.django_db
def test_api_v1_device_type_put(authenticated_client) -> None:
    """
    Test the update device type API endpoint
    :param api_client:
    :return: None
    """
    post_payload = {
        "name": "type_1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }

    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=post_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    assert response_post.data["processors"] == []
    url = response_post.data["url"]
    put_url_path = url.split(site_name)[1]

    processor_module_payload = {
        "name": "rawtojson",
        "description": "parser module",
        "purpose": "PR",
    }
    response_post = api_client.post("/api/v1/stream-processors/", data=processor_module_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    url = response_post.data["url"]

    put_payload = {
        "name": "type_1",
        "description": "updated test fleet",
        "additional_data_json": None,
        "processors": [url],
        "documents": [],
    }

    response_put = api_client.put(put_url_path, data=put_payload, format="json")
    logger.info(response_put.data)
    assert response_put.status_code == 200
    assert response_put.data["processors"] == [url]
    assert response_put.data["description"] == "updated test fleet"


@pytest.mark.django_db
def test_api_v1_device_type_patch(authenticated_client) -> None:
    """
    Test the update device type API endpoint
    :param api_client:
    :return: None
    """
    post_payload = {
        "name": "type_1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }

    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=post_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    assert response_post.data["processors"] == []
    url = response_post.data["url"]
    put_url_path = url.split(site_name)[1]

    processor_module_payload = {
        "name": "rawtojson",
        "description": "parser module",
        "purpose": "PR",
    }
    response_post = api_client.post("/api/v1/stream-processors/", data=processor_module_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    url = response_post.data["url"]

    put_payload = {"processors": [url]}

    response_patch = api_client.patch(put_url_path, data=put_payload, format="json")
    logger.info(response_patch.data)
    assert response_patch.status_code == 200
    assert response_patch.data["name"] == "type_1"
    assert response_patch.data["description"] == "test fleet"
    assert response_patch.data["processors"] == [url]


@pytest.mark.django_db
def test_api_v1_device_type_delete(authenticated_client) -> None:
    """
    Test the delete device type API endpoint
    :param api_client:
    :return: None
    """
    post_payload = {
        "name": "type_1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }

    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=post_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    assert response_post.data["processors"] == []
    url = response_post.data["url"]
    url_path = url.split(site_name)[1]

    response_put = api_client.delete(url_path)
    assert response_put.status_code == 204


@pytest.mark.django_db
def test_api_v1_device_type_invalid_post(authenticated_client) -> None:
    """
    Test the post device type API endpoint with ivalid input type
    - do not input a hyperlink to a relationship
    :param api_client:
    :return: None
    """
    post_payload = {
        "name": "type_1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": ["not-a-hyperlink"],
        "documents": [],
    }

    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=post_payload, format="json")
    logger.info(response_post.data["processors"])
    assert response_post.status_code == 400
    assert (
        str(response_post.data["processors"])
        == "[ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')]"
    )
