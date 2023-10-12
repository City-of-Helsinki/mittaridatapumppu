import uuid

from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from deviceregistry.utils.models import BaseTimestampedModel


def picture_path(instance, filename):
    # Format instance.device.id to be 4 digits long
    return "pictures/{0:04d}/{1}".format(instance.device.id, filename)


def document_path(instance, filename):
    # Format instance.device.id to be 4 digits long
    return "documents/{0:04d}/{1}".format(instance.device.id, filename)


class Organization(BaseTimestampedModel):
    """
    An Organization owns a set of Devices and can update properties of them.
    """

    slug = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=200, editable=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, editable=True, verbose_name=_("Description"))

    def __str__(self):
        org_str = self.name
        truncator = Truncator(self.description)
        descr_len = 23  # Limit description length
        org_str += " ({})".format(truncator.chars(descr_len)) if self.description else ""
        return org_str


class Location(BaseTimestampedModel):
    slug = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    locality = models.CharField(max_length=200, blank=True, verbose_name=_("Place name"))
    district = models.CharField(max_length=200, blank=True, verbose_name=_("District name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    lat = models.FloatField(verbose_name=_("Latitude (dd.ddddd)"))  # degrees (°) -90.0 - 90.0
    lon = models.FloatField(verbose_name=_("Longitude (dd.ddddd)"))  # degrees (°) -180.0 - 180.0
    properties = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.lat:.5f}, {self.lon:.5f})"


class StreamProcessor(models.Model):
    DQM = "DQ"
    PARSING = "PR"
    ALARMS = "AL"
    PURPOSE_CHOICES = [
        (DQM, "Data Quality Management"),
        (PARSING, "Parsing"),
        (ALARMS, "Alarms"),
    ]

    name = models.CharField(max_length=200)
    purpose = models.CharField(
        choices=PURPOSE_CHOICES,
        default=PARSING,
    )
    description = models.TextField()

    def __str__(self):
        return f"{self.name}, (type = {self.purpose})"


class Document(BaseTimestampedModel):
    document = models.FileField(upload_to=document_path)
    description = models.CharField()

    def __str__(self):
        return f"{self.description}"


class DeviceType(BaseTimestampedModel):
    slug = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    urls = models.TextField(blank=True)
    parser_module = models.CharField(max_length=200, blank=True)  # Can be overridden in Device
    processors = models.ManyToManyField(StreamProcessor, related_name="modules", blank=True)
    documents = models.ManyToManyField(Document, related_name="docs", blank=True)
    properties = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Device(BaseTimestampedModel):
    UNRELIABLE = "UR"
    RELIABLE = "RE"
    NEEDS_PROCESSING = "NP"
    QUALITY_CHOICES = [
        (UNRELIABLE, "Unreliable"),
        (RELIABLE, "Reliable"),
        (NEEDS_PROCESSING, "Needs Processing"),
    ]

    INACTIVE = "IN"
    ACTIVE = "AC"
    NEEDS_MAINTENANCE = "NM"
    EQUIPMENT_CONDITION_CHOICES = [
        (INACTIVE, "Inactive"),
        (ACTIVE, "Active"),
        (NEEDS_MAINTENANCE, "Needs Maintenance"),
    ]

    device_id = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    type = models.ForeignKey(DeviceType, related_name="device_set", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pseudonym = models.CharField(max_length=200, blank=True)
    description = models.CharField(blank=True)

    equipment_condition = models.CharField(
        choices=EQUIPMENT_CONDITION_CHOICES,
        default=ACTIVE,
    )
    last_active_at = models.DateTimeField(null=True, blank=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    lat = models.FloatField(null=True)  # degrees (°) -90.0 - 90.0
    lon = models.FloatField(null=True)  # degrees (°) -180.0 - 180.0
    # properties = models.JSONField(null=True, blank=True)
    sensor_config = models.JSONField(null=True, blank=True)
    parser_module = models.CharField(max_length=200, blank=True)
    properties = models.JSONField(null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=200, blank=True)
    measurement_resolution = models.FloatField(null=True, blank=True)

    quality_indicator = models.CharField(
        choices=QUALITY_CHOICES,
        default=RELIABLE,
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # TODO: override save method to create a point from lat and lon
    # Note that this needs GeoDjango and PostGIS
    # def save(self, *args, **kwargs):
    #     # Use lat and lon to create a point
    #     if self.lat and self.lon:
    #         self.geom = Point(float(self.lon), float(self.lat), srid=4326)
    #         self.geog = Point(float(self.lon), float(self.lat), srid=4326)

    def __str__(self):
        return f"{self.name}-{self.pseudonym}-{self.type}"


class DeviceImage(BaseTimestampedModel):
    device = models.ForeignKey(Device, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=picture_path)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    properties = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}: {self.description[:30]}"

    def installation_img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')


class MaintenanceLog(BaseTimestampedModel):
    AUTO = "AU"
    MANUAL = "MA"
    TYPE_CHOICES = [
        (AUTO, "machine-generated"),
        (MANUAL, "manual"),
    ]
    title = models.TextField(blank=True)
    log_file = models.FileField(upload_to="logs/%Y-%m-%d_%H", blank=True)
    description = models.TextField()
    type = models.CharField(
        choices=TYPE_CHOICES,
        default=MANUAL,
    )
    device = models.ForeignKey(Device, related_name="logs", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"


auditlog.register(Organization, exclude_fields=["updated_at"])
auditlog.register(Location, exclude_fields=["updated_at"])
auditlog.register(DeviceType, exclude_fields=["updated_at"])
auditlog.register(Device, exclude_fields=["updated_at"])
