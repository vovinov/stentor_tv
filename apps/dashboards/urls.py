from django.urls import path, include

from apps.dashboards.views import view_for_boss, view_for_editor, view_for_mont

app_name = "dashboards"


urlpatterns = [
    path("boss/", view_for_boss, name="view_for_boss"),
    path("editor/", view_for_editor, name="view_for_editor"),
    path("mont/", view_for_mont, name="view_for_mont"),
]
