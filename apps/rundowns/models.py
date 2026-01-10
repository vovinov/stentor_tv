from django.db import models

class Rundown(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
    
class RundownItem(models.Model):
    pass