# Generated by Django 4.2.4 on 2023-08-29 12:23

import devices.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device_id', models.CharField(default=uuid.uuid4, max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pseudonym', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True)),
                ('equipment_condition', models.CharField(choices=[('IN', 'Inactive'), ('AC', 'Active'), ('NM', 'Needs Maintenance')], default='AC')),
                ('last_active_at', models.DateTimeField(blank=True, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
                ('sensor_config', models.JSONField(blank=True, null=True)),
                ('parser_module', models.CharField(blank=True, max_length=200)),
                ('properties', models.JSONField(blank=True, null=True)),
                ('unit_of_measurement', models.CharField(blank=True, max_length=200)),
                ('measurement_resolution', models.FloatField(blank=True, null=True)),
                ('quality_indicator', models.CharField(choices=[('UR', 'Unreliable'), ('RE', 'Reliable'), ('NP', 'Needs Processing')], default='RE')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.FileField(upload_to=devices.models.document_path)),
                ('description', models.CharField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('locality', models.CharField(blank=True, max_length=200, verbose_name='Place name')),
                ('district', models.CharField(blank=True, max_length=200, verbose_name='District name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('lat', models.FloatField(verbose_name='Latitude (dd.ddddd)')),
                ('lon', models.FloatField(verbose_name='Longitude (dd.ddddd)')),
                ('properties', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StreamProcessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('purpose', models.CharField(choices=[('DQ', 'Data Quality Management'), ('PR', 'Parsing'), ('AL', 'Alarms')], default='PR')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField(blank=True)),
                ('log_file', models.FileField(blank=True, upload_to='logs/%Y-%m-%d_%H')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('AU', 'machine-generated'), ('MA', 'manual')], default='MA')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='devices.device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('urls', models.TextField(blank=True)),
                ('parser_module', models.CharField(blank=True, max_length=200)),
                ('properties', models.JSONField(blank=True, null=True)),
                ('documents', models.ManyToManyField(blank=True, related_name='docs', to='devices.document')),
                ('processors', models.ManyToManyField(blank=True, related_name='modules', to='devices.streamprocessor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=devices.models.picture_path)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('properties', models.JSONField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='devices.device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='device',
            name='current_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.location'),
        ),
        migrations.AddField(
            model_name='device',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_set', to='devices.devicetype'),
        ),
    ]
