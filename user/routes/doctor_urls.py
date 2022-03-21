from django.urls import path
from user.viewsets.doctor_views import (
    DoctorDashboard,
    DoctorProfile,
    DoctorProfileUpdateView,
    PrescriptionView,
    accept_appointment,
    doctor_changepassword,
    MyPatientView,
    PrescriptionCreateView
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
    path(
        "doctor-change-password",
        doctor_changepassword,
        name="doctor-change-password",
    ),
    path("my-patient/", MyPatientView.as_view(), name="my-patient"),
    path("prescription-list/", PrescriptionView.as_view(), name="prescription-list"),
    path("prescription-create/", PrescriptionCreateView.as_view(), name="prescription-create"),
    
]
