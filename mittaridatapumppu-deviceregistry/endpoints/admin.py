from django.contrib import admin
from .models import Endpoint, Host

admin.site.register(Host)
admin.site.register(Endpoint)
