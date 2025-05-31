from django.contrib import admin
from .models import News


@admin.register(News)
class AdminCustomNews(admin.ModelAdmin):
	pass


