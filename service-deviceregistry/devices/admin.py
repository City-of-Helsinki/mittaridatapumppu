from django.contrib import admin

from .models import (
    Device,
    Location,
    StreamProcessor,
    InstallationImage,
    Document,
    DeviceType,
    MaintenanceLog,
)


# inline for many to many relationship
class DeviceTypeProcessorAdminInline(admin.TabularInline):
    model = DeviceType.processors.through
    extra = 0


class DeviceTypeDocAdminInline(admin.TabularInline):
    model = DeviceType.documents.through
    extra = 0


# inline for one to many relationship
class InstallationImageAdminInline(admin.TabularInline):
    model = InstallationImage
    extra = 0
    readonly_fields = ("installation_img_preview",)


class MaintenanceLogAdminInline(admin.StackedInline):
    model = MaintenanceLog
    extra = 0


class DeviceAdminInline(admin.StackedInline):
    model = Device
    extra = 0


class DeviceTypeAdmin(admin.ModelAdmin):
    inlines = [
        DeviceAdminInline,
        DeviceTypeProcessorAdminInline,
        DeviceTypeDocAdminInline,
    ]
    exclude = ["processors", "documents"]


class DeviceAdmin(admin.ModelAdmin):
    inlines = (InstallationImageAdminInline, MaintenanceLogAdminInline)
    exclude = ["processors", "documents"]
    readonly_fields = (
        "created_at",
        "modified_at",
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
    list_display = ("device", "lat", "lon", "area_name")


class StreamProcessorAdmin(admin.ModelAdmin):
    inlines = [DeviceTypeProcessorAdminInline]
    list_display = ("name", "purpose", "description")


class InstallationImageAdmin(admin.ModelAdmin):
    list_display = ("device", "description")
    readonly_fields = ("installation_img_preview",)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(StreamProcessor, StreamProcessorAdmin)
admin.site.register(InstallationImage, InstallationImageAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(MaintenanceLog)
