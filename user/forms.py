from django import forms
from .models import Profile
from django.forms import ValidationError


class UserRegisterationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Profile
        fields = [
            "username",
            "password",
            "confirm_password",
            "user_type",
            "phone_number",
            "profile_pic",
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
