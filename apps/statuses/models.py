from django.db import models

class Status(models.Model):
    code = models.SlugField(max_length=32, unique=True)     
    title = models.CharField(max_length=64)                
    color = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.title