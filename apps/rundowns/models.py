from datetime import timedelta
from django.db import models
from django.db.models import UniqueConstraint

from apps.common.models import AuditModel
from apps.news.models import News

from djangoql.queryset import DjangoQLQuerySet
from simple_history.models import HistoricalRecords


class Rundown(AuditModel):
    air_hour = models.IntegerField(default=0)
    air_day = models.IntegerField(default=0)
    air_month = models.IntegerField(default=0)
    air_year = models.IntegerField(default=0)
    duration = models.DurationField(default=timedelta(0))
    news = models.ManyToManyField(News, through="RundownNews")
    history = HistoricalRecords()

    objects = DjangoQLQuerySet.as_manager()

    class Meta:
        ordering = ["-air_year", "-air_month", "-air_day", "-air_hour"]

        constraints = [
            UniqueConstraint(
                fields=['air_hour', 'air_day', 'air_month', 'air_year'],
                name='unique_airt_time'
            )
        ]

    def __str__(self):
        return f"Выпуск {self.air_year} {self.air_month} {self.air_day} {self.air_hour}"


class RundownNews(models.Model):
    rundown = models.ForeignKey(
        Rundown, on_delete=models.CASCADE, related_name="rundown_news"
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="rundown_news"
    )
    position = models.PositiveIntegerField(default=1)
    history = HistoricalRecords()

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"RundownNews --- {self.rundown} || Новость: {self.news}"

    def __repr_(self):
        return f"RundownNews --- {self.rundown} || Новость: {self.news}"
