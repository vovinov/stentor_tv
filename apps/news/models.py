from django.db import models

STATUS_CHOICES = {
    "mont": "Монтаж",
    "edit": "Правка",
    "final": "Выпуск",
}

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default="mont")
    
    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
