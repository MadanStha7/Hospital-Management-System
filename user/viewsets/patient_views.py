from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, FormView
from user.forms import PatientForm, DoctorForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.db import transaction
from user.models import Patient, Doctor
from django.contrib import messages
from django.http import HttpResponseRedirect

User = get_user_model()


class HomeView(TemplateView):
    """
    Home view
    """

    template_name = "user/index.html"


class RegisterTypeView(TemplateView):
    template_name = "user/register-type.html"


class LoginView(FormView):
    template_name = "user/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
            if User.objects.filter(groups__name="Patient"):
                return HttpResponseRedirect(reverse_lazy("patient-dashboard"))
            elif User.objects.filter(groups__name="Doctor"):
                return HttpResponseRedirect(reverse_lazy("home"))

        else:
            messages.add_message(
                self.request,
                messages.INFO,
                "Wrong credentials, please try again!",
            )
            return HttpResponseRedirect(reverse_lazy("login"))


class PatientRegisterView(CreateView):
    """
    View to store the details of patient
    """

    template_name = "user/patient-register.html"
    form_class = PatientForm
    success_url = reverse_lazy("login")

    @transaction.atomic
    def post(self, request):
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.data.get("email")
            pword = form.data.get("password")
            user_obj = User.objects.create_user(
                email=email, username=email, password=pword
            )
            user = form.save(commit=False)
            user.user = user_obj
            user.save()
            messages.success(request, "User has been successfully Created")
            return redirect("login")

        else:
            user_form = form
            context = {"form": user_form}
        return render(request, "user/patient-register.html", context)


class DoctorRegisterView(CreateView):
    """
    View to store the details of doctor
    """

    template_name = "user/doctor-register.html"
    form_class = DoctorForm
    success_url = reverse_lazy("login")

    @transaction.atomic
    def post(self, request):
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            pword = form.cleaned_data["password"]
            user_obj = User.objects.create_user(
                email=email, username=email, password=pword
            )
            user = form.save(commit=False)
            user.user = user_obj
            user.save()
            messages.success(request, "User has been successfully Created")
            return redirect("login")

        else:
            user_form = form
            context = {"form": user_form}
        return render(request, "user/doctor-register.html", context)


def Logout(request):
    """logout out user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy("home"))


class PatientDashboard(TemplateView):
    template_name = "patient/appointment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            user = Patient.objects.get(user=self.request.user)
        except Patient.DoesNotExist:
            user = None
        context["user"] = user
        return context
