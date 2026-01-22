from django.urls import path, include

from apps.rundowns.views import rundowns_create, rundowns_detail, rundowns_manage

app_name = "rundowns"

urlpatterns = [
    path("manage/", rundowns_manage, name="rundowns_manage"),
    path("detail/<int:rundown_id>/", rundowns_detail, name="rundowns_detail"),
    path("create/", rundowns_create, name="rundowns_create"),
]

# <int:rundown_year>/<int:rundown_month>/<int:rundown_day>/<int:rundown_hour>/
