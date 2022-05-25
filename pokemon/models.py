from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length= 30)
    img = models.TextField()
    

    
class Join(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)