from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 1000)
    phone = models.IntegerField()
    email = models.EmailField()
    
    def __str__(self):
        return self.name