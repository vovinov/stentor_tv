from django.contrib.auth import get_user_model
from django.db import models
from apps.news.models import News


class Rundown(models.Model):
    air_hour = models.IntegerField(default=0)
    air_day = models.IntegerField(default=0)
    air_month = models.IntegerField(default=0)
    air_year = models.IntegerField(default=0)
    duration = models.DurationField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    news = models.ManyToManyField(News, through="RundownNews")
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, related_name="rundown"
    )

    class Meta:
        ordering = ["-air_year", "-air_month", "-air_day", "-air_hour"]

    def __str__(self):
        return f"Выпуск {self.air_year} {self.air_month} {self.air_day} {self.air_hour}"


class RundownNews(models.Model):
    rundown = models.ForeignKey(
        Rundown, on_delete=models.CASCADE, related_name="rundown"
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="rundown_news"
    )
    position = models.PositiveIntegerField(default=1000)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["rundown", "news"],
                name="uniq_rundown_news",
            )
        ]

    def __str__(self):
        return f"RundownNews --- {self.rundown} {self.news}"


class Category(models.Model):
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title
