from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

######################################
### Custom User
######################################

class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        if not email:
            raise ValueError("must have user email")
        if not username:
            raise ValueError("musth have username")
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,
                        username=None,
                        email=None, 
                        address=None, 
                        phone_number=None,
                        password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            address=address,
            phone_number=phone_number,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, null=False,unique=True)
    username = models.CharField(max_length=10, null=False)
    
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_lable):
        return True


######################################
### Diary
######################################

class Diary(models.Model):
    title = models.CharField(max_length=30)
    contents = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_created=True)

