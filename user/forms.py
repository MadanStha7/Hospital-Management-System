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
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    # dob = forms.CharField(widget=DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Patient
        fields = [
            "email",
            "password",
            "confirm_password",
            "full_name",
            "phone",
            "blood_group",
            "image",
        ]

        def __init__(self, *args, **kwargs):
            super(PatientForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].error_messages = {
                    "required": "This Field is required"
                }

        widgets = {
            "blood_group": forms.Select(
                attrs={
                    "class": "form-control",
                }
            )
        }

    def clean_email(self):
        email = User.objects.filter(email=self.cleaned_data.get("email"))
        if email.exists():
            raise forms.ValidationError("email already exist")
        return email

    # check the password match
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("password didnot match")
        return confirm_password


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
    hospital_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    dob = forms.CharField(widget=DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Doctor
        fields = [
            "email",
            "password",
            "full_name",
            "phone",
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
