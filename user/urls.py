from django.urls import path
from user.routes.admin_urls import urlpatterns as admin_urls
from user.routes.patient_urls import urlpatterns as user_urls
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = admin_urls + user_urls
