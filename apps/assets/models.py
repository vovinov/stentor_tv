from datetime import timedelta
from django.db import models

from apps.common.models import AuditModel


class Asset(AuditModel):
    title = models.CharField(max_length=200, unique=True)
    duration = models.DurationField(default=timedelta(0))

    def __str__(self):
        return self.title
