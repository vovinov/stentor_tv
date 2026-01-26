from django.urls import path, include

from apps.rundowns.views import (
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
]

# <int:rundown_year>/<int:rundown_month>/<int:rundown_day>/<int:rundown_hour>/
