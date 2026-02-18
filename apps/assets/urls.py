from django.urls import path

from apps.assets.views import create_asset

app_name = "assets"

urlpatterns = [
    path("create/", create_asset, name="create_asset"),
]
