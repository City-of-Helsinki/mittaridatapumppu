from rest_framework import viewsets
from rest_framework import permissions
from .models import Host, Endpoint
from .serializers import HostSerializer, EndpointSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.order_by("created_at")
    lookup_field = "slug"  # Use slug instead of pk
    serializer_class = HostSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]


class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.order_by("created_at")
    serializer_class = EndpointSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
