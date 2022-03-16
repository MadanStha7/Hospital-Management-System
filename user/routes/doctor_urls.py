from django.urls import path
from user.viewsets.doctor_views import DoctorDashboard, DoctorProfile

urlpatterns = [
    path("doctor-dashboard/", DoctorDashboard.as_view(), name="doctor-dashboard"),
    path("doctor-profile/", DoctorProfile.as_view(), name="doctor-profile"),
]
