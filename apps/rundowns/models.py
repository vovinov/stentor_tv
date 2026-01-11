from datetime import datetime, timedelta
from django.db import models

from apps.news.models import News

class Rundown(models.Model):
    air_date = models.DateTimeField() 
    news = models.ManyToManyField(News, blank=True, through="RundownNews", related_name="rundowns")
    
    def __str__(self):
        return f"{self.air_date}"
    
    
class RundownNews(models.Model):
    rundown = models.ForeignKey(Rundown, on_delete=models.CASCADE, related_name="items")
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    # позиция
    position = models.PositiveIntegerField(default=0)

    # длительность
    duration = models.DurationField(default=timedelta(0))

    class Meta:
        ordering = ["position"]
        unique_together = ("rundown", "news")