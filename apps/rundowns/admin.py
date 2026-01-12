from django.contrib import admin

from .models import Rundown, RundownItem

admin.site.register(Rundown)
admin.site.register(RundownItem)
