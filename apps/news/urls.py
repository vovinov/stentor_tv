from django.urls import path, include

from .views import (
    NewsUpdateView,
    create_news,
    manage_news,
    news_delete,
    search_news,
)

app_name = "news"

urlpatterns = [
    path("manage/", manage_news, name="manage_news"),
    path("manage/search", search_news, name="search_news"),
    path("create/new", create_news, name="create_news"),
    path("<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("<int:item_id>/delete/", news_delete, name="news_delete"),
]
