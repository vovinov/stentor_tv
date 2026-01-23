from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse


from apps.users.forms import UserLoginForm


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = "users/users_login.html"


def user_logout(request):
    logout(request)
    return redirect("users:login")
