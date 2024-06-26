from rest_framework import serializers

from .models import Host, Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        lookup_field = "slug"  # Use slug instead of pk
        fields = "__all__"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class HostSerializer(serializers.ModelSerializer):
    endpoints = EndpointSerializer(many=True, read_only=True)

    class Meta:
        model = Host
        lookup_field = "slug"  # Use slug instead of pk
        fields = [
            "url",
            "slug",
            "host_name",
            "ip_address",
            "description",
            "notification_url",
            "endpoints",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"url": {"lookup_field": "slug"}}
