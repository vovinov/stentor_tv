from django.urls import path, include

from apps.rundowns.views import (
    get_rundowns_by_date,
    rundowns_create,
    rundowns_detail,
    rundowns_manage,
)

app_name = "rundowns"

urlpatterns = [
    path("rundowns/", get_rundowns_by_date, name="get_rundowns_by_date"),
    path("manage/", rundowns_manage, name="rundowns_manage"),
    path("detail/<int:rundown_id>/", rundowns_detail, name="rundown_detail"),
    path("create/", rundowns_create, name="rundowns_create"),
]

# <int:rundown_year>/<int:rundown_month>/<int:rundown_day>/<int:rundown_hour>/
