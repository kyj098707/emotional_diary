from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        if not email:
            raise ValueError("must have user email")
        if not username:
            raise ValueError("must have user username")
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username=None, email=None, password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=10)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="userfollower",default=0)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="userfollowing",default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_lable):
        return True

    def send_welcomemail(self,pk,token):
        title = "안녕"
        content = render_to_string('__01_account/activate_email.html',
                                    {
                                    'pk': pk,
                                    'token': token,
                                    })
        sender = settings.WELCOME_EMAIL_SENDER
        send_mail(title,content,sender,[self.email],fail_silently=False)
