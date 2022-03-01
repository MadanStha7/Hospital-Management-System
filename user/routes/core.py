from .admin_urls import urlpatterns as admin_urls
from .patient_urls import urlpatterns as user_urls

urlpatterns = (admin_urls + user_urls)
