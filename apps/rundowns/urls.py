from django.urls import path, include

from apps.rundowns.views import (
    change_news_position_down,
    change_news_position_up,
    get_rundowns_by_date,
    create_rundown,
    get_rundown_detail,
    manage_rundowns,
)

app_name = "rundowns"

urlpatterns = [
    path("rundowns/", get_rundowns_by_date, name="get_rundowns_by_date"),
    path("manage/", manage_rundowns, name="manage_rundowns"),
    path("detail/<int:rundown_id>/", get_rundown_detail, name="get_rundown_detail"),
    path("create/", create_rundown, name="create_rundown"),
    path(
        "<int:rundown_news_id>/change/down/",
        change_news_position_down,
        name="change_news_position_down",
    ),
    path(
        "<int:rundown_news_id>/change/up/",
        change_news_position_up,
        name="change_news_position_up",
    ),
]

# <int:rundown_year>/<int:rundown_month>/<int:rundown_day>/<int:rundown_hour>/
