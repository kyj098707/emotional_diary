from django.db import models
from accounts.models import User

class Diary(models.Model):
    title = models.CharField(max_length=20)
    cotent = models.TextField()
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.IntegerField(default=0,null=True)
    created_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
