from django.db import models
from django.contrib.auth import get_user_model


class TimedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserBaseModel(models.Model):
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_modified",
    )

    def save(self, user=None, *args, **kwargs):
        if not self.pk:
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AuditModel(TimedBaseModel, UserBaseModel):

    class Meta:
        abstract = True
