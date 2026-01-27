from django.contrib import admin

from apps.users.models import Position, User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin): ...


@admin.register(Position)
class CustomPositionAdmin(admin.ModelAdmin): ...
