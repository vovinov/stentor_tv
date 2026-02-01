from django.contrib import admin
from django.utils import timezone

from .models import Rundown, RundownNews


admin.site.register(Rundown)


@admin.register(RundownNews)
class CustomRundownNewsAdmin(admin.ModelAdmin):
    fields = ["rundown", "news", "start_time", "end_time", "position"]
