# Generated by Django 4.2.5 on 2023-09-19 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('host_name', models.CharField(max_length=300)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('notification_url', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('endpoint_path', models.CharField(help_text='Path to endpoint, e.g. /api/v1/data', max_length=200)),
                ('http_request_handler', models.CharField(blank=True, help_text='Name of Python handler function', max_length=200)),
                ('auth_token', models.CharField(blank=True, max_length=200)),
                ('data_source', models.CharField(blank=True, max_length=200)),
                ('properties', models.JSONField(blank=True, help_text='Envs as JSON object (KEY - value pairs)', null=True)),
                ('allowed_ip_addresses', models.TextField(blank=True, default='0.0.0.0/0', help_text='One IP address per line, can use CIDR notation')),
                ('kafka_raw_data_topic', models.CharField(blank=True, max_length=200)),
                ('kafka_parsed_data_topic', models.CharField(blank=True, max_length=200)),
                ('kafka_group_id', models.CharField(blank=True, max_length=200)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endpoints', to='endpoints.host')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
