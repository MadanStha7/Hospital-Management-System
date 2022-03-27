from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView
from user.models import (
    Doctor,
    Appointment,
    Prescription,
    Hospital,
    Hospital_Appointment,
)
from user.forms import DoctorProfileForm, PrescriptionCreateForm, HospitalProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from user.decorators import LoginRequiredMixin


class HospitalDashboard(LoginRequiredMixin, TemplateView):
    template_name = "hospital/hospital-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        try:
            user = Hospital.objects.get(user=logged_user)
        except Hospital.DoesNotExist:
            user = None

        context["user"] = user
        context["appointment_list"] = Hospital_Appointment.objects.filter(
            hospital__user=logged_user
        )
        context["total_appointment"] = Hospital_Appointment.objects.filter(
            hospital__user=logged_user
        ).count()
        context["pending_appointment"] = Hospital_Appointment.objects.filter(
            hospital__user=logged_user, status="P"
        ).count()
        today = date.today()
        context["today_appointment"] = Hospital_Appointment.objects.filter(
            hospital__user=logged_user, a_date=today
        ).count()
        return context


class HospitalProfile(LoginRequiredMixin, TemplateView):
    template_name = "hospital/hospital-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        hospital = Hospital.objects.get(user=logged_user)
        context["hospital"] = hospital
        return context


# class HospitalProfileUpdateView(UpdateView):
#     template_name = "hospital/hospital-update.html"
#     model = Hospital
#     form_class = HospitalProfileForm
#     success_url = reverse_lazy("hospital-pfoile")

#     def form_valid(self, form):
#         user = self.request.user
#         form.save()

#         return super().form_valid(form)


def hospital_profile(request):
    form = HospitalProfileForm(instance=request.user)
    if request.method == "POST":
        form = HospitalProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("hospital-profile")
        else:
            print("errors", form.errors)
    return render(request, "hospital/hospital-profile.html", {"form": form})


def hospital_changepassword(request):
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
    return render(request, "hospital/change-password.html", {"form": form})

def accept_hospital_appointment(request, pk):
    appointment = Hospital_Appointment.objects.get(id=pk)
    if request.method == "POST":
        appointment.status = "A"
        appointment.save()
        messages.success(request, "Appointment Accepted")
        return redirect("hospital-dashboard")