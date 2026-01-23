from django.db import models
from django.contrib.auth import get_user_model

from apps.assets.models import Asset


class News(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Описание новости")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    asset = models.OneToOneField(
        Asset, on_delete=models.SET_NULL, null=True, related_name="news"
    )
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
