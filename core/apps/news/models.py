from django.db import models


# Create your models here.
class News(models.Model):

    status_choices = {
        "CRT": "created",
        "WRT": "writing",
        "EDT": "editing",
        "UPD": "updating",
        "ONL": "on air"
    }

    title = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=status_choices)

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = "Новость"
        verbose_name_plural = "Новости"



