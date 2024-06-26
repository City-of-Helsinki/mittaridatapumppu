import ipaddress

from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models

from deviceregistry.utils.models import BaseTimestampedModel


class Host(BaseTimestampedModel):
    slug = models.SlugField(max_length=64, unique=True)
    host_name = models.CharField(max_length=300)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    description = models.TextField(blank=True)
    notification_url = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.host_name} ({self.notification_url})"


class Endpoint(BaseTimestampedModel):
    host = models.ForeignKey(Host, related_name="endpoints", on_delete=models.CASCADE)
    endpoint_path = models.CharField(max_length=200, help_text="Path to endpoint, e.g. /api/v1/data")
    http_request_handler = models.CharField(blank=True, max_length=200, help_text="Name of Python handler function")
    auth_token = models.CharField(blank=True, max_length=200)
    data_source = models.CharField(blank=True, max_length=200)
    properties = models.JSONField(null=True, blank=True, help_text="Envs as JSON object (KEY - value pairs)")
    allowed_ip_addresses = models.TextField(
        blank=True, default="0.0.0.0/0", help_text="One IP address per line, can use CIDR notation"
    )
    kafka_raw_data_topic = models.CharField(blank=True, max_length=200)
    kafka_parsed_data_topic = models.CharField(blank=True, max_length=200)
    kafka_group_id = models.CharField(blank=True, max_length=200)

    def clean(self):
        """Validate that there are one ip address per line and that they are valid"""
        if self.allowed_ip_addresses:
            ip_addrs = self.allowed_ip_addresses.split()
            clean_addresses = []
            for ip_addr in ip_addrs:
                if not ip_addr:
                    continue
                try:
                    if "/" in ip_addr:
                        ipaddress.ip_network(ip_addr)
                    else:
                        ipaddress.ip_address(ip_addr)
                    clean_addresses.append(ip_addr)
                except ValueError:
                    raise ValidationError(f"Invalid IP address: {ip_addr}")
            self.allowed_ip_addresses = "\n".join(clean_addresses)
        if self.allowed_ip_addresses.strip() == "":  # Explicitly set to "all ip addresses" instead of empty string
            self.allowed_ip_addresses = "0.0.0.0/0"

    def __str__(self):
        return f"{self.host} {self.endpoint_path}"


auditlog.register(Endpoint, exclude_fields=["updated_at"])
auditlog.register(Host, exclude_fields=["updated_at"])
