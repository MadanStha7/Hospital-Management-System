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
    DownloadPdf
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
    path("invoice/<int:pk>", InvoiceView.as_view(), name="invoice"),
    path('download/pdf/', DownloadPdf, name='download-pdf'),

]
