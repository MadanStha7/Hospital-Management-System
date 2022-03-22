from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Class to authenticate only to logged in user
    """

    def test_func(self):
        if self.request.user:
            return True
        return False

    def handle_no_permission(self):
        return redirect("login")
