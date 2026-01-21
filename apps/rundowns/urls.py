from django.urls import path, include

from apps.rundowns.views import rundown_get, rundowns_create, rundowns_manage

app_name = "rundowns"

urlpatterns = [
    path("manage/", rundowns_manage, name="rundowns_manage"),
    path("create/", rundowns_create, name="rundowns_create"),
    path("<int:rundown_id>/", rundown_get, name="rundown_get"),
]

# <int:rundown_year>/<int:rundown_month>/<int:rundown_day>/<int:rundown_hour>/
