from django.urls import path
from user.viewsets.user_views import LoginView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
]
