from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from user.models import Doctor, Appointment
from user.forms import DoctorProfileForm
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages


class DoctorDashboard(TemplateView):
    template_name = "doctor/doctor-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = Doctor.objects.get(user=self.request.user)
        except Doctor.DoesNotExist:
            user = None

        context["user"] = user
        context["appointment_list"] = Appointment.objects.all()
        context["total_appointment"] = Appointment.objects.all().count()
        context["pending_appointment"] = Appointment.objects.filter(status="P").count()
        today = date.today()
        context["today_appointment"] = Appointment.objects.filter(
            app_date=today
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

