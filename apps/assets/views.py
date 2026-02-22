from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone

from apps.assets.forms import AssetCreationForm


def create_asset(request):

    form = AssetCreationForm(request.POST, request.FILES)

    if form.is_valid():
        asset = form.save(commit=False)
        asset.mont = request.user
        asset.created_by = request.user
        asset.updated_by = request.user
        asset.mont = request.user
        asset.save()

    response = render(request, "news/news_manage.html")
    response["HX-Trigger"] = "success"

    messages.success(request, "Материал успешно создан!")

    return response
