from .admin_urls import urlpatterns as admin_urls
from .patient_urls import urlpatterns as user_urls
from .doctor_urls import urlpatterns as doctor_urls

urlpatterns = admin_urls + user_urls + doctor_urls
