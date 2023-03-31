from django.contrib import admin
from .models import Diary,Comment,Tag
# Register your models here.

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass