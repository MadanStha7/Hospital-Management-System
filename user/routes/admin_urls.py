from django.urls import path
from user.viewsets.admin_views import AdminView

urlpatterns = [path("admins/", AdminView.as_view(), name="admin-dashboard")]
