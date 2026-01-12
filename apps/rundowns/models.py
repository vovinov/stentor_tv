from datetime import datetime, timedelta
from django.db import models

from apps.news.models import News


class Rundown(models.Model):
    air_date = models.DateTimeField()

    class Meta:
        ordering = ["air_date"]

    def __str__(self):
        return f"{self.air_date}"


class RundownItem(models.Model):
    rundown = models.ForeignKey(
        Rundown, on_delete=models.CASCADE, related_name="randown_items"
    )
    news = models.ForeignKey(News, on_delete=models.PROTECT)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
