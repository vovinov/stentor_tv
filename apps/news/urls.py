from django.urls import path, include

from .views import (
    manage_news,
    search_news,
    create_news,
    show_news_to_add_rundown,
    add_news_to_rundown,
    NewsUpdateView,
    delete_news_from_rundown,
)

app_name = "news"

urlpatterns = [
    path("manage/", manage_news, name="manage_news"),
    path("manage/search", search_news, name="search_news"),
    path("create/", create_news, name="create_news"),
    path(
        "show/<int:rundown_id>/",
        show_news_to_add_rundown,
        name="show_news_to_add_rundown",
    ),
    path(
        "add/<int:rundown_id>/<int:news_id>/",
        add_news_to_rundown,
        name="add_news_to_rundown",
    ),
    path("<int:pk>/edit/", NewsUpdateView.as_view(), name="edit_news"),
    path("<int:item_id>/delete/", delete_news_from_rundown, name="delete_news"),
]
