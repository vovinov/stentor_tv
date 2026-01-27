from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=150, verbose_name="Статус")
    color = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.title
