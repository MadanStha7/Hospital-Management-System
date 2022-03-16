from pydoc import Doc
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from user.models import Doctor
from user.forms import DoctorProfileForm


class DoctorDashboard(TemplateView):
    template_name = "doctor/doctor-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            user = Doctor.objects.get(user=self.request.user)
        except Doctor.DoesNotExist:
            user = None
        context["user"] = user
        return context


class DoctorProfile(TemplateView):
    template_name = "doctor/doctor-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        doctor = Doctor.objects.get(user=logged_user)
        context["doctor"] = doctor
        return context
