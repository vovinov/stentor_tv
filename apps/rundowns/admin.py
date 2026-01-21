from django.contrib import admin
from django.utils import timezone

from utils import round_to_hour

from .models import Rundown, RundownNews, Category


@admin.register(Rundown)
class RundownAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.air_time = round_to_hour(timezone.now())

        super().save_model(request, obj, form, change)


admin.site.register(RundownNews)
admin.site.register(Category)
