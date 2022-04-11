import io
from os import stat
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from user.forms import (
    PatientForm,
    DoctorForm,
    UserLoginForm,
    PatientEditFormView,
    HospitalForm,
)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View, DetailView
from django.db import transaction
from user.models import Patient, Doctor, Appointment, Prescription
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from user.decorators import LoginRequiredMixin

User = get_user_model()


class HomeView(TemplateView):
    """
    Home view
    """

    template_name = "user/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all().order_by("-date_created")[:4]
        return context


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
            if user.groups.filter(name="Doctor"):
                return HttpResponseRedirect(reverse_lazy("doctor-dashboard"))
            elif user.groups.filter(name="Patient"):
                return HttpResponseRedirect(reverse_lazy("patient-dashboard"))
            elif user.groups.filter(name="Hospital"):
                return HttpResponseRedirect(reverse_lazy("hospital-dashboard"))
            elif self.request.user.is_superuser:
                return HttpResponseRedirect(reverse_lazy("admin-dashboard"))
            else:
                pass

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


class HospitalRegisterView(CreateView):
    """
    View to store the details of hospital
    """

    template_name = "user/hospital-register.html"
    form_class = HospitalForm
    success_url = reverse_lazy("login")

    @transaction.atomic
    def post(self, request):
        form = HospitalForm(request.POST, request.FILES)
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
        return render(request, "user/hospital-register.html", context)


def Logout(request):
    """logout out user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy("home"))


# photo category
"""===================================
------ Patient appointment section  ---
======================================"""


class PatientDashboard(LoginRequiredMixin, TemplateView):
    template_name = "patient/appointment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            appoinment_list = Appointment.objects.filter(
                patient__user=self.request.user
            )
        except Appointment.DoesNotExist:
            appoinment_list = None
        context["appoinment_list"] = appoinment_list
        return context


class FindDoctor(LoginRequiredMixin, TemplateView):
    template_name = "patient/find-doctor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class SearchDoctor(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        location = self.request.GET.get("location", "")
        speciality = self.request.GET.get("specility", "")
        filtered_list = Doctor.objects.filter(
            Q(location__icontains=location) | Q(specialist__icontains=speciality)
        )
        return render(
            self.request,
            "patient/find-doctor.html",
            context={
                "doctors": filtered_list,
                "location": location,
                "speciality": speciality,
            },
        )


def make_appointment(request, pk):
    """Make appounemnt with doctor"""
    try:
        doctor_obj = Doctor.objects.get(id=pk)
    except Doctor.DoesNotExist:
        return False
    if request.method == "POST":

        appointment_date = request.POST["appointment_date"]
        app_obj = Appointment.objects.create(
            doctor=doctor_obj,
            patient=Patient.objects.get(user__id=request.user.id),
            app_date=appointment_date,
            status="P",
        )
        messages.success(request, "Appointment request has been successfully sent")
        return HttpResponseRedirect(reverse_lazy("patient-dashboard"))
    return render(request, "patient/make-appointment.html", {"doctor_obj": doctor_obj})


class InvoiceView(DetailView):
    model = Appointment
    template_name = "patient/patient-invoice.html"
    context_object_name = "invoice"


"""===================================
------ Patient Prescription section  ---
======================================"""


class PrescriptionDashboard(LoginRequiredMixin, TemplateView):
    template_name = "patient/prescriptions/pre-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prescriptions_list"] = Prescription.objects.filter(
            appointement__patient__user=self.request.user
        )
        return context


class PatientPrescriptionsInvoiceView(LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = "patient/prescriptions/patient-pre-invoice.html"
    context_object_name = "invoice"


def patient_profile(request):
    form = PatientEditFormView(instance=request.user.patient)
    if request.method == "POST":
        form = PatientEditFormView(
            request.POST, request.FILES, instance=request.user.patient
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("patient-profile")
        else:
            print("errors", form.errors)
    return render(request, "patient/profile.html", {"form": form})


def patient_changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "patient/change-password.html", {"form": form})


class ApplyCard(LoginRequiredMixin, TemplateView):
    template_name = "patient/card/apply-card.html"


def card_confirm(request):
    pat = Patient.objects.filter(user_id=request.user.id).update(card_status="P")
    return render(request, "patient/card/thank_card.html")


class CardView(LoginRequiredMixin, TemplateView):
    template_name = "patient/card/card-view.html"


class ContactView(TemplateView):
    template_name = "user/contact.html"
