from .models import Endpoint
from rest_framework import serializers


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = "__all__"
