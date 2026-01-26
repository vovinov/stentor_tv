from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=150)
    color = models.CharField(max_length=10)
