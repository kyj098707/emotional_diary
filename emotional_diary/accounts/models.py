from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class User(AbstractUser):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    nickname = models.CharField(max_length=10)

    def send_welcomemail(self,domain,pk,token):
        title = "안녕"
        content = render_to_string('__01_account/activate_email.html',
                                    {
                                    'domain':domain,
                                    'pk': pk,
                                    'token': token,
                                    })
        sender = settings.WELCOME_EMAIL_SENDER
        print(sender,self.email)
        send_mail(title,"",sender,[self.email],fail_silently=False)
