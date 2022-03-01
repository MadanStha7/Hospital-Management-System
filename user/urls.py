from django.urls import path
from user.routes.admin_urls import urlpatterns as admin_urls
from user.routes.patient_urls import urlpatterns as user_urls

urlpatterns = admin_urls + user_urls


