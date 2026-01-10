from django.db import models

class Rundown(models.Model):
    air_date = models.DateTimeField(null=True)
    

    def __str__(self):
        return f"{self.air_date}"
    
class RundownItem(models.Model):
    pass