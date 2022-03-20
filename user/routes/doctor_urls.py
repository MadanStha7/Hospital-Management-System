from django.urls import path
from user.viewsets.doctor_views import (
    DoctorDashboard,
    DoctorProfile,
    DoctorProfileUpdateView,
    accept_appointment,
)

urlpatterns = [
    path("doctor-dashboard/", DoctorDashboard.as_view(), name="doctor-dashboard"),
    path("doctor-profile/", DoctorProfile.as_view(), name="doctor-profile"),
    path(
        "doctor-profile/<int:pk>/update/",
        DoctorProfileUpdateView.as_view(),
        name="doctor-update",
    ),
    path("accept/appointment/<int:pk>/", accept_appointment, name="accept-appointment"),
]
