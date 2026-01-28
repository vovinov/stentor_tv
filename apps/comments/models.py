from django.db import models

from apps.common.models import TimedBaseModel
from apps.news.models import News
from apps.users.models import User

from django.contrib.auth import get_user_model


class Comment(TimedBaseModel):
    text = models.TextField()
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, null=True, related_name="comment"
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comment_created_by"
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comment_updated_by",
        null=True,
    )

    def __str__(self):
        return self.text
