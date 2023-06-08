from rest_framework.test import APIClient
import pytest
import logging
from django.contrib.auth.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


site_name = "testserver"
rootfolder = "/project"


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


def create_device_type(authenticated_client) -> str:
    """
    create a new device type and return hyperlink
    """
    device_type_payload = {
        "name": "type1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }
    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=device_type_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    return response_post.data["url"]


def test_api_v1_device_unauthenticated(api_client) -> None:
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

    response_post = api_client.post("/api/v1/devices/", data=payload, format="json")
    assert response_post.status_code == 403


@pytest.mark.django_db
def test_api_v1_device_post_all_fields(authenticated_client) -> None:
    """
    Test the create device type API endpoint
    :param api_client:
    :return: None
    """
    device_type_payload = {
        "name": "type1",
        "description": "test fleet",
        "additional_data_json": None,
        "processors": [],
        "documents": [],
    }
    api_client = authenticated_client
    response_post = api_client.post("/api/v1/device-types/", data=device_type_payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201
    type_url = response_post.data["url"]

    payload = {
        "device_id": "id1234",
        "name": "sensor2",
        "pseudonym": "q1",
        "description": "test fleet from akaniemi",
        "type": type_url,
        "sensor_config": None,
        "additional_data_json": None,
        "equipment_condition": "AC",
        "quality_indicator": "RE",
        "owner": "http://testserver/api/v1/users/1/",
        "unit_of_measurement": "m",
        "measurement_resolution": 0.1,
        "installation_image_set": [],
        "maintenance_log_set": [],
        "last_active_at": "2021-01-01T00:00:00Z",
        "lat": 60.0,
        "lon": 24.0,
    }

    response_post = api_client.post("/api/v1/devices/", data=payload, format="json")
    logger.info(response_post.data)
    assert response_post.status_code == 201, "post succeeds"
    device_url = response_post.data["url"]
    assert device_url == "http://testserver/api/v1/devices/id1234/", "lookupfield is device_id"

    response_get = api_client.get(device_url)
    logger.info(response_get.data)
    assert response_get.data["owner"] == "http://testserver/api/v1/users/1/"


@pytest.mark.django_db
def test_api_v1_device_add_installation_image(authenticated_client) -> None:
    """
    Test the create device type API endpoint
    :param api_client:
    :return: None
    """

    type_url = create_device_type(authenticated_client)

    payload = {
        "device_id": "id1234",
        "name": "sensor2",
        "pseudonym": "q1",
        "description": "test fleet from akaniemi",
        "type": type_url,
        "sensor_config": None,
        "additional_data_json": None,
        "equipment_condition": "AC",
        "quality_indicator": "RE",
        "owner": "http://testserver/api/v1/users/2/",
        "unit_of_measurement": "m",
        "measurement_resolution": 0.1,
        "installation_image_set": [],
        "maintenance_log_set": [],
        "last_active_at": "2021-01-01T00:00:00Z",
        "lat": 60.0,
        "lon": 24.0,
    }

    api_client = authenticated_client
    response_post = api_client.post("/api/v1/devices/", data=payload, format="json")
    logger.info(f" post device  {response_post.data}")
    assert response_post.status_code == 201
    device_url = response_post.data["url"]
    assert device_url == "http://testserver/api/v1/devices/id1234/"

    file = f"{rootfolder}/devices/tests/testresources/testimage.jpeg"
    image_payload = {
        "image": (open(file, "rb"), file),
        "description": "test fleet",
        "device": device_url,
    }
    response_post = api_client.post("/api/v1/installation-images/", data=image_payload)
    logger.info(f" post image  {response_post.data}")
    assert response_post.status_code == 201
    image_url = response_post.data["url"]

    response_get = api_client.get(device_url)
    assert response_get.data["installation_image_set"][0] == image_url
