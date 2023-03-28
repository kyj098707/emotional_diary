from django.contrib import admin
from .models import Diary,Comment, Like
# Register your models here.

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
