from django.contrib import admin
from .models import User, Follower, Following
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    pass
