
from django.contrib.auth.models import AbstractUser
from django.db import models

class Closer(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    
    
    def __str__(self):
        return self.username

