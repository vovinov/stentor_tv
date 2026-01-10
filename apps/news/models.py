from django.db import models

from django.conf import settings

STATUS_CHOICES = {
    "mont": "Монтаж",
    "edit": "Правка",
    "final": "Эфир",
}

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default="mont")
    
    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

class AssetRef(models.Model):
    title = models.CharField(max_length=250)
    duration = models.DurationField()
    created_at = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=100)
    news_id = models.ForeignKey("News", on_delete=models.DO_NOTHING)