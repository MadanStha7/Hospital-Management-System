from django import forms
from .models import UserProfile
from django.forms import ValidationError
from django.forms import DateInput


class DateInput(forms.DateInput):
    input_type = "date"


class UserRegisterationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["is_staff", "is_active", "date_joined"]

        def __init__(self, *args, **kwargs):
            super(UserRegisterationForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].error_messages = {
                    "required": "This Field is required"
                }

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "blood_group": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "shift": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "dob": DateInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "user_type": forms.Select(
                attrs={
                    "class": "form-control",
                    "onchange": "onchangeUserType(this.value)",
                }
            ),
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
