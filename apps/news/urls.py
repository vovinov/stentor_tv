from django.urls import path, include

from .views import (
    NewsUpdateView,
    news_content,
    news_create,
    news_create_form,
    news_delete,
)

app_name = "news"

urlpatterns = [
    path("content/", news_content, name="news_content"),
    path("create/", news_create_form, name="news_create_form"),
    path("create/new", news_create, name="news_create"),
    path("<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("<int:item_id>/delete/", news_delete, name="news_delete"),
]
