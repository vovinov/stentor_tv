from django.db import models
from apps.common.models import TimedBaseModel
from apps.news.models import News

from django.utils import timezone

from django.contrib.auth import get_user_model

from djangoql.queryset import DjangoQLQuerySet


class Rundown(TimedBaseModel):
    air_hour = models.IntegerField(default=0)
    air_day = models.IntegerField(default=0)
    air_month = models.IntegerField(default=0)
    air_year = models.IntegerField(default=0)
    duration = models.DurationField(blank=True, null=True)
    news = models.ManyToManyField(News, through="RundownNews")
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="rundown_creator"
    )
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="rundown_updater"
    )

    objects = DjangoQLQuerySet.as_manager()

    class Meta:
        ordering = ["-air_year", "-air_month", "-air_day", "-air_hour"]

    def __str__(self):
        return f"Выпуск {self.air_year} {self.air_month} {self.air_day} {self.air_hour}"


class RundownNews(models.Model):
    rundown = models.ForeignKey(
        Rundown, on_delete=models.CASCADE, related_name="rundown_news"
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="rundown_news"
    )
    start_time = models.TimeField(default=timezone.localtime())
    end_time = models.TimeField(default=timezone.localtime())
    position = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["rundown", "news"],
                name="uniq_rundown_news",
            )
        ]

    def __str__(self):
        return f"RundownNews --- {self.rundown} || Новость: {self.news}"

    def __repr_(self):
        return f"RundownNews --- {self.rundown} || Новость: {self.news}"


class Category(models.Model):
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title
