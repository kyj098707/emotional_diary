from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, gender=None,password=None):
        if not email:
            raise ValueError("fill email")
        if not username:
            raise ValueError("fill username")
        user= self.model(
            username=username,
            email=self.normalize_email(email),
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username=None,email=None,password=None):
        user = self.create_user(
            username=username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin= True
        user.is_staff =True
        user.is_superuser=True
        user.is_active =True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    username = models.CharField(max_length=10, unique=True)
    gender = models.BooleanField(null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    obejects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_lable):
        return True
    


