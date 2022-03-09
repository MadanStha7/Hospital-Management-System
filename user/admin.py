from django.contrib import admin
from django.apps import apps
from .models import User, Patient, Doctor


admin.site.register([User, Patient, Doctor])
