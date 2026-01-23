from django.urls import path, include

from .views import LoginUser, user_logout

app_name = "users"

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
]
