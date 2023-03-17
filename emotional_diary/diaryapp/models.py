from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Diary(models.Model):
    title = models.CharField(max_length=20)
    cotent = models.TextField()
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name
    
## 다대다 필드

class Like_user_diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE)
    like = models.BooleanField()

class Re_diary_tag(models.Model):
    diary = models.ForeignKey(Diary,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete = models.CASCADE)
