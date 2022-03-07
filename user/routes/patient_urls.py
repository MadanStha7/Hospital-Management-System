from django.urls import path
from user.viewsets.patient_views import HomeView, LoginView, RegisterView, Logout,PatientDashboard

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", Logout, name="logout"),
    path("patient-dashboard/",PatientDashboard.as_view(),name="patient-dashboard")
]
