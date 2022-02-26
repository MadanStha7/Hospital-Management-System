from django.shortcuts import render
from django.views.generic import TemplateView


class AdminView(TemplateView):
    template_name = "admin/dashboard.html"
