from django.contrib.auth import get_user_model
from django.db import models
from apps.news.models import News


class Rundown(models.Model):
    air_date = models.CharField(max_length=10, null=True)
    air_time = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    news = models.ManyToManyField(News, through="RundownNews")
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-air_date"]

    def __str__(self):
        return f"{self.air_date} ---- {self.air_time}"


class RundownNews(models.Model):
    rundown = models.ForeignKey(
        Rundown, on_delete=models.CASCADE, related_name="rundowns_items"
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="rundowns_items"
    )
    position = models.PositiveIntegerField(default=1000)
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
