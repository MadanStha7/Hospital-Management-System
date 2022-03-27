from django.urls import path
from user.viewsets.hospital_views import (
    HospitalDashboard,
    HospitalProfile,
    # HospitalProfileUpdateView,
    hospital_changepassword,
    hospital_profile,
    accept_hospital_appointment
)

urlpatterns = [
    path("hospital-dashboard/", HospitalDashboard.as_view(), name="hospital-dashboard"),
    path("hospital-profile/", hospital_profile, name="hospital-profile"),
    # path(
    #     "hospital-profile/<int:pk>/update/",
    #     HospitalProfileUpdateView.as_view(),
    #     name="hospital-update",
    # ),
    path(
        "hospital-change-password",
        hospital_changepassword,
        name="hospital-change-password",
    ),
    path("accept/hospital/appointment/<int:pk>/", accept_hospital_appointment, name="accept-hospital-appointment"),
    
]
