from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView
from user.models import Doctor, Appointment, Prescription
from user.forms import DoctorProfileForm, PrescriptionCreateForm
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class DoctorDashboard(TemplateView):
    template_name = "doctor/doctor-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        try:
            user = Doctor.objects.get(user=logged_user)
        except Doctor.DoesNotExist:
            user = None

        context["user"] = user
        context["appointment_list"] = Appointment.objects.filter(
            doctor__user=logged_user
        )
        context["total_appointment"] = Appointment.objects.filter(
            doctor__user=logged_user
        ).count()
        context["pending_appointment"] = Appointment.objects.filter(
            doctor__user=logged_user, status="P"
        ).count()
        today = date.today()
        context["today_appointment"] = Appointment.objects.filter(
            doctor__user=logged_user, app_date=today
        ).count()

        return context


class DoctorProfile(TemplateView):
    template_name = "doctor/doctor-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        doctor = Doctor.objects.get(user=logged_user)
        context["doctor"] = doctor
        return context


class DoctorProfileUpdateView(UpdateView):
    template_name = "doctor/doctor-update.html"
    model = Doctor
    form_class = DoctorProfileForm
    success_url = reverse_lazy("doctor-profile")

    def form_valid(self, form):
        user = self.request.user
        form.save()

        return super().form_valid(form)


def accept_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    print(appointment, "...............................")
    print(request.method)
    if request.method == "POST":
        appointment.status = "A"
        appointment.save()
        messages.success(request, "Appointment Accepted")
        return redirect("doctor-dashboard")


def doctor_changepassword(request):
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
    return render(request, "doctor/change-password.html", {"form": form})


class MyPatientView(TemplateView):
    template_name = "doctor/my-patient.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        context["appointment_list"] = Appointment.objects.filter(doctor__user=logged_user, status="A")
        return context


class PrescriptionView(TemplateView):
    template_name = "doctor/prescription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        context["prescription_list"] = Prescription.objects.filter(appointement__doctor__user=logged_user)
        return context

class PrescriptionCreateView(CreateView):
    template_name = 'doctor/prescriptioncreate.html'
    form_class = PrescriptionCreateForm
    success_url = reverse_lazy('prescription-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        doctor = Doctor.objects.get(user=self.request.user)
        form.instance.doctor = doctor
        return super().form_valid(form)