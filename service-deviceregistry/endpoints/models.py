from django.db import models


class Endpoint(models.Model):
    endpoint_path = models.CharField()
    http_request_handler = models.CharField()
    allowed_ip_addrs = models.CharField()
    auth_token = models.CharField()
    data_source = models.CharField()
    kafka_raw_data_topic = models.CharField()
    kafka_parsed_data_topic = models.CharField()
    kafka_group_id = models.CharField()

    def __str__(self):
        return f"src: {self.data_source} endpoint:{self.endpoint_path})"
