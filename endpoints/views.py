from rest_framework import viewsets
from rest_framework import permissions
from .models import Endpoint
from .serializers import EndpointSerializer


class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = [permissions.IsAuthenticated]
