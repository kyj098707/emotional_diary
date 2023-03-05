from django.db import models

# Diary Model
class Diary(models.Model):
    title = models.CharField(max_length=30)
    contents = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_created=True)