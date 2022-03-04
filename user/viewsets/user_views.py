from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, FormView
from user.forms import UserRegisterationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from user.models import UserProfile
from django.contrib import messages
from django.http import HttpResponseRedirect


class HomeView(TemplateView):
    """
    Home view
    """

    template_name = "user/index.html"


class LoginView(FormView):
    template_name = "user/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(
                self.request,
                messages.INFO,
                "Wrong credentials, please try again!",
            )
            return HttpResponseRedirect(reverse_lazy("login"))


class RegisterView(CreateView):
    template_name = "user/register.html"
    form_class = UserRegisterationForm
    success_url = reverse_lazy("login")

    def post(self, request):
        user_form = UserRegisterationForm(request.POST, request.FILES)
        if user_form.is_valid():
            newuser = UserProfile(
                email=user_form.data["email"],
                password=user_form.data["password"],
                full_name=user_form.data["full_name"],
                phone=user_form.data["phone"],
                dob=user_form.data["dob"],
                blood_group=user_form.data["blood_group"],
                # shift=user_form.data["shift"],
                image=user_form.data["image"],
                user_type=user_form.data["user_type"],
            )
            print("user", newuser)
            newuser.save()
            messages.success(request, "User has been successfully Created")
            return redirect("login")

        else:
            book_form1 = user_form
            context = {"form": book_form1}
        return render(request, "user/register.html", context)


def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy("home"))
