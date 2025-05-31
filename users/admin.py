from django.contrib import admin

from .models import User

@admin.register(User)
class AdminCustomUser(admin.ModelAdmin):
	pass


