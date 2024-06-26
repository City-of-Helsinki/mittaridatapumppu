from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Device,
    DeviceImage,
    DeviceType,
    Document,
    Location,
    MaintenanceLog,
    Organization,
    StreamProcessor,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password"]
        extra_kwargs = {"url": {"lookup_field": "username"}}


class StreamProcessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StreamProcessor
        fields = "__all__"


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        lookup_field = "slug"  # Use slug instead of pk
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        lookup_field = "slug"  # Use slug instead of pk
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        lookup_field = "slug"  # Use slug instead of pk
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = [
            "url",
            "device_id",
            "type",
            "name",
            "lat",
            "lon",
            "pseudonym",
            "description",
            "created_at",
            "updated_at",
            "equipment_condition",
            "last_active_at",
            "current_location",
            "sensor_config",
            "unit_of_measurement",
            "measurement_resolution",
            "quality_indicator",
            "equipment_condition",
            "owner",
            # "organization",
            "parser_module",
            "properties",
            "logs",
            "images",
        ]
        lookup_field = "device_id"
        extra_kwargs = {
            "url": {"lookup_field": "device_id"},
            "type": {"lookup_field": "slug"},
            "owner": {"lookup_field": "username"},
            "current_location": {"lookup_field": "slug"},
            # "organization": {"lookup_field": "slug"},
        }


class InstallationImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceImage
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
