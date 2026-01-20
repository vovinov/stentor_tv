from datetime import datetime, timedelta
from django.db import models

from apps.news.models import News


class Rundown(models.Model):
    air_date = models.DateTimeField()
    news = models.ManyToManyField(News, through="RundownNews")

    class Meta:
        ordering = ["-air_date"]

    def __str__(self):
        return f"{self.air_date}"


class RundownNews(models.Model):
    rundown = models.ForeignKey(
        Rundown, on_delete=models.CASCADE, related_name="rundowns_items"
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="rundowns_items"
    )
    position = models.PositiveIntegerField(default=0)
    block = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["rundown", "news"],
                name="uniq_rundown_news",
            )
        ]

    def __str__(self):
        return f"{self.rundown} {self.news}"


class Category(models.Model):
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title
