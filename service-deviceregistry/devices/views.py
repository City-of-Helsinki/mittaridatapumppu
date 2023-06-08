from .models import (
    Device,
    Location,
    InstallationImage,
    Document,
    StreamProcessor,
    DeviceType,
    MaintenanceLog,
)
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)

from .serializers import (
    DeviceSerializer,
    LocationSerializer,
    UserSerializer,
    InstallationImageSerializer,
    DocumentSerializer,
    StreamProcessorSerializer,
    DeviceTypeSerializer,
    MaintenanceLogSerializer,
)
from django.contrib.auth.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class DeviceTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows device types to be viewed or edited.
    """

    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows devices to be viewed or edited.
    """

    queryset = Device.objects.all().order_by("-created_at")
    lookup_field = "device_id"
    serializer_class = DeviceSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class InstallationImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows installation images to be viewed or edited.
    """

    queryset = InstallationImage.objects.all()
    serializer_class = InstallationImageSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows documents to be viewed or edited.
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class StreamProcessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows processor modules to be viewed or edited.
    """

    queryset = StreamProcessor.objects.all()
    serializer_class = StreamProcessorSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows maintenance logs to be viewed or edited.
    """

    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
