from django.db import models
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from user.forms import UserRegisterationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from user.models import UserProfile
from django.contrib import messages


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


class RegisterView(CreateView):
    template_name = "user/register.html"
    form_class = UserRegisterationForm
    success_url = reverse_lazy("login")

    def post(self, request):
        user_form = UserRegisterationForm(request.POST, request.FILES)
        if user_form.is_valid():
            print("user form", user_form.data)
            newuser = UserProfile(
                email=user_form.data["email"],
                password=user_form.data["password"],
                full_name=user_form.data["full_name"],
                phone=user_form.data["phone"],
                dob=user_form.data["dob"],
                blood_group=user_form.data["blood_group"],
                # shift=user_form.data["shift"],
                image=user_form.data["image"],
                user_type=user_form.data["user_type"],
            )
            print("user", newuser)
            newuser.save()
            messages.success(request, "User has been successful Created")
            return reverse_lazy("home")

        else:
            print("forms error", user_form.errors)
            print(user_form.errors.as_json())
            book_form1 = user_form
            context = {"form": book_form1}
        return render(request, "user/register.html", context)
