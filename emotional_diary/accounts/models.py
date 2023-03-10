from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    nickname = models.CharField(max_length=10)

    def send_welcomemail(self):
        title = "안녕하세요! 감정일기입니다"
        content = ""
        sender = settings.WELCOME_EMAIL_SENDER
        send_mail(title,content,sender,[self.email],fail_silently=False)
