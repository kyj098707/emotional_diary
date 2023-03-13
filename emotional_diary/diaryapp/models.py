from django.db import models
from django.conf import settings

class Diary(models.Model):
    title = models.CharField(max_length=20)
    cotent = models.TextField()
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    like = models.IntegerField(default=0,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name