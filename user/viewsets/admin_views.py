import io
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from user.models import Doctor, Patient, Appointment, Hospital
from django.urls import reverse_lazy


class AdminView(TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all().count()
        context["patients"] = Patient.objects.all().count()
        context["appointments"] = Appointment.objects.all().count()
        context["hospitals"] = Hospital.objects.all().count()
        return context


class DoctorListView(TemplateView):
    template_name = "admin/doctor-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class PatientListView(TemplateView):
    template_name = "admin/patient-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients"] = Patient.objects.all()
        return context


class HospitalListView(TemplateView):
    template_name = "admin/hospital-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hospitals"] = Hospital.objects.all()
        return context


class DoctorDetailView(DetailView):
    template_name = "admin/doctor-detail.html"
    model = Doctor
    context_object_name = "doctor"


class DoctorDeleteView(DeleteView):
    model = Doctor
    success_url = reverse_lazy("doctor-list")


class PatientDetailView(DetailView):
    template_name = "admin/patient-detail.html"
    model = Patient
    context_object_name = "patient"


class patientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy("patient-list")


class HospitalDetailView(DetailView):
    template_name = "admin/hospital-detail.html"
    model = Hospital
    context_object_name = "hospital"


class HospitalDeleteView(DeleteView):
    model = Hospital
    success_url = reverse_lazy("hospital-list")
