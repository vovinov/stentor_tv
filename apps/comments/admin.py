from django.contrib import admin

from apps.comments.models import Comment


@admin.register(Comment)
class CustomCommentAdmin(admin.ModelAdmin):
    pass
