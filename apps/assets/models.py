from datetime import timedelta
from django.db import models


class Asset(models.Model):
    title = models.CharField(max_length=200, unique=True)
    duration = models.DurationField(blank=True)

    def __str__(self):
        return self.title
