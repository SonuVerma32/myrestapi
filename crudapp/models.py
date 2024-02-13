from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 1000)
    phone = models.IntegerField()
    email = models.EmailField()
    createdDate = models.DateTimeField()
    
    def __str__(self):
        return self.name
    

class U2(models.Model):
    name = models.CharField(max_length = 1000)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.name