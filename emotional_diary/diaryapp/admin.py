from django.contrib import admin
from .models import Diary,Comment
# Register your models here.

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    pass

