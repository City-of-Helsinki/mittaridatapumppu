# Generated by Django 4.2.1 on 2023-06-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Endpoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("endpoint_path", models.CharField()),
                ("http_request_handler", models.CharField()),
                ("allowed_ip_addrs", models.CharField()),
                ("auth_token", models.CharField()),
                ("data_source", models.CharField()),
                ("kafka_raw_data_topic", models.CharField()),
                ("kafka_parsed_data_topic", models.CharField()),
                ("kafka_group_id", models.CharField()),
            ],
        ),
    ]
