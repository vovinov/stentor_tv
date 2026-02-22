from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import AuditModel


class Asset(AuditModel):
    title = models.CharField(max_length=200, unique=True)
    duration = models.DurationField(default=timedelta(0))
    video = models.FileField(upload_to='videos/', null=True)

    def __str__(self):
        return self.title
