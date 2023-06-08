from .models import (
    Device,
    Location,
    InstallationImage,
    Document,
    StreamProcessor,
    DeviceType,
    MaintenanceLog,
)
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class StreamProcessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StreamProcessor
        fields = "__all__"


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = [
            "url",
            "device_id",
            "type",
            "name",
            "pseudonym",
            "description",
            "created_at",
            "modified_at",
            "equipment_condition",
            "last_active_at",
            "current_location",
            "sensor_config",
            "unit_of_measurement",
            "measurement_resolution",
            "quality_indicator",
            "equipment_condition",
            "owner",
            "parser_module",
            "maintenance_log_set",
            "installation_image_set",
        ]
        lookup_field = "device_id"
        extra_kwargs = {"url": {"lookup_field": "device_id"}}


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class InstallationImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstallationImage
        fields = "__all__"
        extra_kwargs = {
            "device": {"lookup_field": "device_id"},
            "parent": {"lookup_field": "device_id"},
        }


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class MaintenanceLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = "__all__"
        extra_kwargs = {
            "device": {"lookup_field": "device_id"},
            "parent": {"lookup_field": "device_id"},
        }
