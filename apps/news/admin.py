from django.contrib import admin

from .models import News


@admin.register(News)
class CustomNewsAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
