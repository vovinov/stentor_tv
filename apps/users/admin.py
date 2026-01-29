from django.contrib import admin

from apps.users.models import Position, User
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)


@admin.register(Position)
class CustomPositionAdmin(admin.ModelAdmin): ...
