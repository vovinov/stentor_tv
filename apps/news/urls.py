from django.urls import path, include

from .views import (
    NewsUpdateView,
    create_news,
    manage_news,
    delete_news_from_rundown,
    search_news,
)

app_name = "news"

urlpatterns = [
    path("manage/", manage_news, name="manage_news"),
    path("manage/search", search_news, name="search_news"),
    path("create/", create_news, name="create_news"),
    path("<int:pk>/edit/", NewsUpdateView.as_view(), name="edit_news"),
    path("<int:item_id>/delete/", delete_news_from_rundown, name="delete_news"),
]
