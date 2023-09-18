from django.test import TestCase
import tempfile
from devices.models import (
    Device,
    Location,
    StreamProcessor,
    Document,
    InstallationImage,
    DeviceType,
    MaintenanceLog,
)
from django.contrib.auth.models import User
from PIL import Image
from django.test import override_settings


class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create(
            lat=10.0,
            lon=20.0,
            area_name="Rautatientori",
        )

    def test_read_device_location(self):
        device_location = Location.objects.get(area_name="Rautatientori")
        self.assertEqual(str(device_location), "Location(10.0, 20.0), area = Rautatientori")


class StreamProcessorTestCase(TestCase):
    def test_read_stream_processor(self):
        StreamProcessor.objects.create(
            name="jsonparser",
            purpose="formatting",
            description="parses raw data into json",
        )
        stream_processor = StreamProcessor.objects.get(name="jsonparser")
        self.assertEqual(str(stream_processor), "jsonparser, (type = formatting)")


class InstallationImageTestCase(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_read_installationimage(self):
        """Test that an installation image can be added to the database."""
        user = User.objects.create(username="testuser", password="12345")
        dev_type = DeviceType.objects.create(name="type", description="type_demo")
        Device.objects.create(
            device_id="test_device_id",
            type=dev_type,
            pseudonym="test_pseudonym",
            description="description",
            owner=user,
        )

        temp_file = tempfile.NamedTemporaryFile()
        img = Image.new(mode="RGB", size=(300, 300), color=(209, 123, 193))
        img.save(temp_file, "jpeg")
        device = Device.objects.get(device_id="test_device_id")
        InstallationImage.objects.create(
            image=temp_file.name,
            description="test_installation_img_description",
            device=device,
        )

        image = InstallationImage.objects.get(description="test_installation_img_description")
        self.assertIsNotNone(image.image)


class DocumentTestCase(TestCase):
    def test_read_device_document(self):
        Document.objects.create(
            document="test_document",
            description="test_document_description",
        )

        device_document = Document.objects.get(document="test_document")
        self.assertEqual(str(device_document), "test_document_description")


class DeviceTestCase(TestCase):
    def test_read_device(self):
        user = User.objects.create(username="testuser", password="12345")
        dev_type = DeviceType.objects.create(name="type", description="type_demo")

        Device.objects.create(
            device_id="test_device_id",
            name="tempsensor",
            type=dev_type,
            pseudonym="sss10",
            owner=user,
        )
        device = Device.objects.get(device_id="test_device_id")
        self.assertEqual(str(device), "tempsensor-sss10-type")
        self.assertEqual(device.owner.username, "testuser")
        self.assertEqual(device.type.name, "type")


class DeviceTypeTestCase(TestCase):
    def setUp(self):
        processor = StreamProcessor.objects.create(
            name="jsonparser",
            purpose="formatting",
            description="parses raw data into json",
        )

        dev_type = DeviceType.objects.create(name="test_device_type", description="test_device_type_description")

        doc1 = Document.objects.create(
            document="doc1",
            description="test_document_description",
        )
        doc2 = Document.objects.create(
            document="doc2",
            description="test_document_description",
        )

        dev_type.processors.add(processor)
        dev_type.documents.add(doc1, doc2)

    def test_read_device_type(self):
        device_type = DeviceType.objects.get(name="test_device_type")
        self.assertEqual(str(device_type), "test_device_type")
        self.assertEqual(device_type.description, "test_device_type_description")
        self.assertEqual(int(device_type.processors.count()), 1)
        self.assertEqual(int(device_type.documents.count()), 2)


class MaintenanceLogTestCase(TestCase):
    def test_read_maintenance_log(self):
        user = User.objects.create(username="testuser", password="12345")
        dev_type = DeviceType.objects.create(name="type", description="type_demo")
        sensor = Device.objects.create(
            device_id="test_device_id",
            type=dev_type,
            pseudonym="test_pseudonym",
            description="description",
            owner=user,
        )

        MaintenanceLog.objects.create(
            log_text="some text here",
            log_file="test_description",
            device=sensor,
            description="log",
        )
        maintenance_log = MaintenanceLog.objects.all().first()
        self.assertEqual(str(maintenance_log), "log")
        self.assertEqual(maintenance_log.device.device_id, "test_device_id")
