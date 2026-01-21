from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from apps.users.forms import UserLoginForm


def user_login(request):

    if request.method == "POST":

        form = UserLoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user and user.is_active:
                login(request, user)
                return redirect("index")
    else:
        form = UserLoginForm()

    return render(request, "users/users_login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("users:login")
