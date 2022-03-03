from django.shortcuts import render
from django.views.generic import TemplateView
from user.forms import UserRegisterationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout


class HomeView(TemplateView):
    """
    Home view
    """

    template_name = "user/index.html"


class LoginView(TemplateView):
    template_name = "user/login.html"
    form_class = UserLoginForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        self.thisuser = user
        if user is not None:
            login(self.request, user)
        else:
            return render(
                self.request,
                self.template_name,
                {"form": form, "error": "Invalid Credentials"},
            )
        return super().form_valid(form)


class RegisterView(TemplateView):
    template_name = "user/register.html"
