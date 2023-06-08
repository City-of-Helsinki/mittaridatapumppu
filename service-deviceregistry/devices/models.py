from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.html import mark_safe


class Location(models.Model):
    lat = models.FloatField()  # degrees (°) -90.0 - 90.0
    lon = models.FloatField()  # degrees (°) -180.0 - 180.0
    area_name = models.CharField(max_length=200)

    def __str__(self):
        return f"Location({self.lat}, {self.lon}), area = {self.area_name}"


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


class Document(models.Model):
    document = models.FileField(upload_to="documents/%Y-%m-%d_%H", blank=True)
    description = models.CharField()

    def __str__(self):
        return f"{self.description}"


class DeviceType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    processors = models.ManyToManyField(StreamProcessor, related_name="modules", blank=True)
    documents = models.ManyToManyField(Document, related_name="docs", blank=True)
    additional_data_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Device(models.Model):
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
    current_location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    lat = models.FloatField(null=True)  # degrees (°) -90.0 - 90.0
    lon = models.FloatField(null=True)  # degrees (°) -180.0 - 180.0
    sensor_config = models.JSONField(null=True, blank=True)
    parser_module = models.CharField(max_length=200, blank=True)
    additional_data_json = models.JSONField(null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=200, blank=True)
    measurement_resolution = models.FloatField(null=True, blank=True)

    quality_indicator = models.CharField(
        choices=QUALITY_CHOICES,
        default=RELIABLE,
    )

    equipment_condition = models.CharField(
        choices=EQUIPMENT_CONDITION_CHOICES,
        default=ACTIVE,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    # TODO: override save method to create a point from lat and lon
    # Note that this needs GeoDjango and PostGIS
    # def save(self, *args, **kwargs):
    #     # Use lat and lon to create a point
    #     if self.lat and self.lon:
    #         self.geom = Point(float(self.lon), float(self.lat), srid=4326)
    #         self.geog = Point(float(self.lon), float(self.lat), srid=4326)

    def __str__(self):
        return f"{self.name}-{self.pseudonym}-{self.type}"


class InstallationImage(models.Model):
    description = models.CharField()
    image = models.ImageField(upload_to="installation_pics/%Y-%m-%d_%H", blank=True)
    device = models.ForeignKey(Device, related_name="installation_image_set", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"

    def installation_img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')


class MaintenanceLog(models.Model):
    AUTO = "AU"
    MANUAL = "MA"
    TYPE_CHOICES = [
        (AUTO, "machine-generated"),
        (MANUAL, "manual"),
    ]
    log_text = models.TextField(blank=True)
    log_file = models.FileField(upload_to="logs/%Y-%m-%d_%H", blank=True)
    description = models.CharField()
    type = models.CharField(
        choices=TYPE_CHOICES,
        default=MANUAL,
    )
    device = models.ForeignKey(Device, related_name="maintenance_log_set", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}"
