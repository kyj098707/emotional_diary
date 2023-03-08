from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    nickname = models.CharField(max_length=10)