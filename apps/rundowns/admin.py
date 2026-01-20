from django.contrib import admin

from .models import Rundown, RundownNews, Category

admin.site.register(Rundown)
admin.site.register(RundownNews)
admin.site.register(Category)
