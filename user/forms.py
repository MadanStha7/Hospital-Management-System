from django import forms
from django.db.models import fields
from .models import Patient, Doctor
from django.forms import ValidationError
from django.forms import DateInput
from django.contrib.auth import get_user_model

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"


class PatientForm(forms.ModelForm):

    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    blood_group = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    dob = forms.CharField(widget=DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Patient
        fields = [
            "email",
            "password",
            "full_name",
            "phone",
            "blood_group",
            "dob",
            "image",
        ]

        def __init__(self, *args, **kwargs):
            super(PatientForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].error_messages = {
                    "required": "This Field is required"
                }

    def clean_email(self):
        email = User.objects.filter(email=self.cleaned_data.get("email"))
        if email.exists():
            raise forms.ValidationError("email already exist")
        return email


class DoctorForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    blood_group = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    location = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    hospital_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    dob = forms.CharField(widget=DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Doctor
        fields = [
            "email",
            "password",
            "full_name",
            "phone",
            "blood_group",
            "dob",
            "image",
            "shift",
            "hospital_name",
            "location",
        ]

        def __init__(self, *args, **kwargs):
            super(PatientForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].error_messages = {
                    "required": "This Field is required"
                }

        def clean_email(self):
            email = User.objects.filter(email=self.cleaned_data.get("email"))
            if email.exists():
                raise forms.ValidationError("email already exist")
            return email

        widgets = {
            "shift": forms.Select(
                attrs={
                    "class": "form-control",
                }
            )
        }


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
