from django.db import models

from apps.common.models import AuditModel
from apps.news.models import News


class Comment(AuditModel):
    text = models.TextField()
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, null=True, related_name="comment"
    )

    def __str__(self):
        return self.text
