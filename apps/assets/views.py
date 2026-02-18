from django.shortcuts import render
from django.contrib import messages

from apps.assets.forms import AssetCreationForm


def create_asset(request):

    form = AssetCreationForm(request.POST)

    if form.is_valid():
        asset = form.save()

    response = render(request, "assets/assets_item.html")
    response["HX-Trigger"] = "success"

    messages.success(request, "Материал успешно создан!")

    return response
