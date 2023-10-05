from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import (
    Device,
    Location,
    StreamProcessor,
    DeviceImage,
    Document,
    DeviceType,
    MaintenanceLog,
    Organization,
)


# inline for many-to-many relationship
class DeviceTypeProcessorAdminInline(admin.TabularInline):
    model = DeviceType.processors.through
    extra = 0


class DeviceTypeDocAdminInline(admin.TabularInline):
    model = DeviceType.documents.through
    extra = 0


# inline for one-to-many relationship
class InstallationImageAdminInline(admin.TabularInline):
    model = DeviceImage
    extra = 0
    readonly_fields = ("installation_img_preview",)


class MaintenanceLogAdminInline(admin.StackedInline):
    model = MaintenanceLog
    extra = 0


class DeviceAdminInline(admin.StackedInline):
    model = Device
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("name", "description", "created_at", "updated_at")


class DeviceTypeAdmin(admin.ModelAdmin):
    inlines = [
        DeviceAdminInline,
        DeviceTypeProcessorAdminInline,
        DeviceTypeDocAdminInline,
    ]
    exclude = ["processors", "documents"]
    list_display = ("id", "slug", "name", "parser_module", "created_at")


class DeviceAdmin(admin.ModelAdmin):
    inlines = (InstallationImageAdminInline, MaintenanceLogAdminInline)
    exclude = ["processors", "documents"]
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_display = (
        "device_id",
        "pseudonym",
        "equipment_condition",
        "last_active_at",
    )


class DocumentAdmin(admin.ModelAdmin):
    inlines = (DeviceTypeDocAdminInline,)
    list_display = ("description", "document")


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "lat", "lon")


class StreamProcessorAdmin(admin.ModelAdmin):
    inlines = [DeviceTypeProcessorAdminInline]
    list_display = ("name", "purpose", "description")


class InstallationImageAdmin(admin.ModelAdmin):
    list_display = ("device", "description")
    readonly_fields = ("installation_img_preview",)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["__str__", "action_time", "user"]
    list_filter = ["user"]


admin.site.register(Device, DeviceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(StreamProcessor, StreamProcessorAdmin)
admin.site.register(DeviceImage, InstallationImageAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(MaintenanceLog)
admin.site.register(Organization, OrganizationAdmin)
