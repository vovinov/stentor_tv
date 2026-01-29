from django.urls import path, include

from .views import (
    add_comment_to_news,
    change_asset_news,
    change_news_status,
    manage_news,
    search_news,
    create_news,
    show_news_to_add_rundown,
    add_news_to_rundown,
    NewsUpdateView,
    delete_news_from_rundown,
    show_assets_to_add_news,
    view_history,
)

app_name = "news"

urlpatterns = [
    path("<int:news_id>/history/", view_history, name="view_history"),
    path("manage/", manage_news, name="manage_news"),
    path("manage/search/", search_news, name="search_news"),
    path("create/", create_news, name="create_news"),
    path(
        "<int:news_id>/assets/", show_assets_to_add_news, name="show_assets_to_add_news"
    ),
    path(
        "<int:news_id>/assets/<int:asset_id>/",
        change_asset_news,
        name="change_asset_news",
    ),
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
    path(
        "<int:item_id>/delete/",
        delete_news_from_rundown,
        name="delete_news_from_rundown",
    ),
    path(
        "<int:news_id>/status/",
        change_news_status,
        name="change_news_status",
    ),
    path(
        "comments/",
        add_comment_to_news,
        name="add_comment_to_news",
    ),
]
