from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import AuditModel
from apps.assets.models import Asset
from apps.statuses.models import Status

from djangoql.queryset import DjangoQLQuerySet
from simple_history.models import HistoricalRecords


class News(AuditModel):
    title = models.CharField(max_length=200, unique=True, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    asset = models.OneToOneField(
        Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name="news"
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    locked_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True, related_name="locked_news")
    locked_until = models.DateTimeField(null=True, blank=True)
    editor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="news")
    history = HistoricalRecords()

    objects = DjangoQLQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title
