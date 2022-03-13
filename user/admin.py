from django.contrib import admin
from django.apps import apps
from .models import User, Patient, Doctor,Appointment


admin.site.register([User, Patient, Doctor,Appointment])
