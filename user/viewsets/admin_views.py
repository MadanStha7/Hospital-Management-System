import uuid
from typing_extensions import Required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from user.models import Doctor, Patient, Appointment, Hospital
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from user.decorators import LoginRequiredMixin
from datetime import timedelta

User = get_user_model()


class AdminView(LoginRequiredMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all().count()
        context["patients"] = Patient.objects.all().count()
        context["appointments"] = Appointment.objects.all().count()
        context["hospitals"] = Hospital.objects.all().count()
        return context


class DoctorListView(LoginRequiredMixin, TemplateView):
    template_name = "admin/doctor-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class PatientListView(LoginRequiredMixin, TemplateView):
    template_name = "admin/patient-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients"] = Patient.objects.all()
        return context


class HospitalListView(LoginRequiredMixin, TemplateView):
    template_name = "admin/hospital-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hospitals"] = Hospital.objects.all()
        return context


class DoctorDetailView(LoginRequiredMixin, DetailView):
    template_name = "admin/doctor-detail.html"
    model = Doctor
    context_object_name = "doctor"


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy("doctor-list")


class PatientDetailView(LoginRequiredMixin, DetailView):
    template_name = "admin/patient-detail.html"
    model = Patient
    context_object_name = "patient"


class patientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy("patient-list")


class HospitalDetailView(LoginRequiredMixin, DetailView):
    template_name = "admin/hospital-detail.html"
    model = Hospital
    context_object_name = "hospital"


class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = Hospital
    success_url = reverse_lazy("hospital-list")


class DoctorAppoinmentView(LoginRequiredMixin, TemplateView):
    template_name = "admin/doctor-appointment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointments"] = Appointment.objects.all()
        return context


class HospitalAppoinmentView(LoginRequiredMixin, TemplateView):
    template_name = "admin/hospital-appointment-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hospital_appoint"] = Hospital.objects.all()
        return context


class PendingCardView(LoginRequiredMixin, TemplateView):
    template_name = "admin/pending-card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_card"] = Patient.objects.filter(card_status="P")
        return context


def accept_pending_card(request, pk):
    uuid_no = str(uuid.uuid4().int)[:6]
    months = datetime.now().date() + timedelta(days=120)
    pat = Patient.objects.filter(id=pk).update(
        card_status="V", health_uid=uuid_no, health_card_exp=months
    )
    return redirect("pending-card")


class AllCardView(LoginRequiredMixin, TemplateView):
    template_name = "admin/all-card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_cards"] = Patient.objects.filter(card_status="V")
        return context


def cancel_card(request, pk):
    Patient.objects.filter(id=pk).update(
        card_status="P", health_uid=None, health_card_exp=None
    )
    return redirect("all-card")


class AdminProfile(LoginRequiredMixin, TemplateView):
    template_name = "admin/admin-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.request.user.id)
        return context


def admin_changepassword(request):
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
    return render(request, "admin/change-password.html", {"form": form})
