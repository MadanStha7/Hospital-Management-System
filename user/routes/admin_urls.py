from django.urls import path
from user.viewsets.admin_views import (
    AdminView,
    DoctorListView,
    PatientListView,
    HospitalListView,
    DoctorDetailView,
    DoctorDeleteView,
    PatientDetailView,
    patientDeleteView,
    HospitalDetailView,
    HospitalDeleteView,
    DoctorAppoinmentView,
    HospitalAppoinmentView,
    PendingCardView,
    accept_pending_card,
    AllCardView,
    cancel_card,
    AdminProfile,
    admin_changepassword
)

urlpatterns = [
    path("admin-dashboard/", AdminView.as_view(), name="admin-dashboard"),
    # doctor
    path("doctor-list/", DoctorListView.as_view(), name="doctor-list"),
    path(
        "doctor-detail/<int:pk>", DoctorDetailView.as_view(), name="admin-doctor-detail"
    ),
    path(
        "doctor-delete/<int:pk>", DoctorDeleteView.as_view(), name="admin-doctor-delete"
    ),
    # patient
    path("patient-list/", PatientListView.as_view(), name="patient-list"),
    path(
        "patient-detail/<int:pk>",
        PatientDetailView.as_view(),
        name="admin-patient-detail",
    ),
    path(
        "patient-delete/<int:pk>",
        patientDeleteView.as_view(),
        name="admin-patient-delete",
    ),
    # hospitals
    path("hospital-list/", HospitalListView.as_view(), name="hospital-list"),
    path(
        "hospital-detail/<int:pk>",
        HospitalDetailView.as_view(),
        name="admin-hospital-detail",
    ),
    path(
        "hospital-delete/<int:pk>",
        HospitalDeleteView.as_view(),
        name="admin-hospital-delete",
    ),
    # doctors
    path(
        "doctor-appointment/",
        DoctorAppoinmentView.as_view(),
        name="admin-doctor-appointment-list",
    ),
    # hospitals appointment
    path(
        "hospitals-appointment/",
        HospitalAppoinmentView.as_view(),
        name="admin-hospital-appointment-list",
    ),
    # health card
    path("pending-card/", PendingCardView.as_view(), name="pending-card"),
    path(
        "accept-pending-card/<int:pk>", accept_pending_card, name="accept-pending-card"
    ),
    path("all-card/", AllCardView.as_view(), name="all-card"),
    path("cancel-card/<int:pk>", cancel_card, name="cancel-card"),
    # profile
    path("admin-profile/", AdminProfile.as_view(), name="admin-profile"),
     # change password
    path(
        "admin-change-password",
        admin_changepassword,
        name="admin-change-password",
    ),
]
