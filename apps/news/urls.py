from django.urls import path, include

from .views import news_create, news_delete

app_name = "news"

urlpatterns = [
    path("create/", news_create, name="news_create"),
    path("delete/<int:item_id>/", news_delete, name="news_delete"),
]
