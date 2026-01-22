from django.contrib import admin
from django.utils import timezone

from .models import Rundown, RundownNews, Category


admin.site.register(Rundown)
admin.site.register(RundownNews)
admin.site.register(Category)
