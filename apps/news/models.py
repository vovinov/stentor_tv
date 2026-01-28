from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import TimedBaseModel
from apps.assets.models import Asset
from apps.statuses.models import Status

from djangoql.queryset import DjangoQLQuerySet


class News(TimedBaseModel):
    title = models.CharField(max_length=200, unique=True, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    asset = models.OneToOneField(
        Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name="news"
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="news_creator"
    )
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="news_updater"
    )

    objects = DjangoQLQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title
