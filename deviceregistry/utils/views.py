from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


class AuthenticatedViewSet(viewsets.ModelViewSet):
    """
    Abstract base class for all viewsets that require authentication and permissions.
    """

    permission_classes = [permissions.DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
