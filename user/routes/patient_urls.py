from django.urls import path
from user.viewsets.patient_views import (
    HomeView,
    LoginView,
    PatientRegisterView,
    DoctorRegisterView,
    Logout,
    PatientDashboard,
    RegisterTypeView,
    FindDoctor,
    SearchDoctor,
    make_appointment,
    InvoiceView,
    PrescriptionDashboard,
    PatientPrescriptionsInvoiceView,
    patient_profile,
    patient_changepassword,
    ApplyCard,
    card_confirm,
    CardView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register-type/", RegisterTypeView.as_view(), name="register-type"),
    path("patient-register/", PatientRegisterView.as_view(), name="patient-register"),
    path("doctor-register/", DoctorRegisterView.as_view(), name="doctor-register"),
    path("logout/", Logout, name="logout"),
    # appoinment
    path("patient-dashboard/", PatientDashboard.as_view(), name="patient-dashboard"),
    path("find-doctor/", FindDoctor.as_view(), name="find-doctor"),
    path("search-doctor/", SearchDoctor.as_view(), name="dr-search"),
    path("appoinment-doctor/<int:pk>", make_appointment, name="make-appointment"),
    path("patient/invoice/<int:pk>", InvoiceView.as_view(), name="invoice"),
    # prescriptions
    path("prescriptions/", PrescriptionDashboard.as_view(), name="prescription"),
    path(
        "patient-prescriptions/invoice/<int:pk>",
        PatientPrescriptionsInvoiceView.as_view(),
        name="patient-prescriptions",
    ),
    # patient profile
    path("patient-profile/", patient_profile, name="patient-profile"),
    # change password
    path(
        "patient-change-password",
        patient_changepassword,
        name="patient-change-password",
    ),
    # apply for card
    path("apply-card/", ApplyCard.as_view(), name="apply-card"),
    path("card-confirm/", card_confirm, name="card-confirm"),
    path("card-view/", CardView.as_view(), name="card-view"),


]
