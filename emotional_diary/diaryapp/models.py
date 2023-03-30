from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Diary(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="like_diary",blank=True)
    tag = models.ManyToManyField(Tag, related_name="diary_tag",blank=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE,null=True)


    

