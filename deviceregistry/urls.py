"""
URL configuration for deviceregistry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from devices.views import (
    DeviceViewSet,
    LocationViewSet,
    UserViewSet,
    InstallationImageViewSet,
    DocumentViewSet,
    StreamProcessorViewSet,
    DeviceTypeViewSet,
    MaintenanceLogViewSet,
    OrganizationViewSet,
    index,
)
from endpoints.views import HostViewSet, EndpointViewSet


router = routers.DefaultRouter()
router.register(r"devices", DeviceViewSet)
router.register(r"device-types", DeviceTypeViewSet)
router.register(r"documents", DocumentViewSet)
router.register(r"installation-images", InstallationImageViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"maintenance-logs", MaintenanceLogViewSet)
router.register(r"organizations", OrganizationViewSet)
router.register(r"stream-processors", StreamProcessorViewSet)
router.register(r"users", UserViewSet)
router.register(r"hosts", HostViewSet)
router.register(r"endpoints", EndpointViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", index, name="index"),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
