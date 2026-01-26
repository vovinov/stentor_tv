from django.contrib import admin

from apps.statuses.models import Status


@admin.register(Status)
class CustomStatusAdmin(admin.ModelAdmin):
    pass
