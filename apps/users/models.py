from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    position = models.ForeignKey(
        "Position", on_delete=models.SET_NULL, blank=True, null=True
    )


class Position(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиция"

    def __str__(self):
        return self.title
