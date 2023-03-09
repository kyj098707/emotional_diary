from django.db import models
from accounts.models import User

class Diary(models.Model):
    title = models.CharField(max_length=20)
    cotent = models.TextField()
    user =  models.ForeignKey(User,on_delete=models.CASCADE)


