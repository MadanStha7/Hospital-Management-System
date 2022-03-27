from django.urls import path
from user.routes.admin_urls import urlpatterns as admin_urls
from user.routes.patient_urls import urlpatterns as user_urls
from user.routes.doctor_urls import urlpatterns as doctor_urls
from user.routes.hospital_urls import urlpatterns as hospital_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = admin_urls + user_urls + doctor_urls+  hospital_urls
