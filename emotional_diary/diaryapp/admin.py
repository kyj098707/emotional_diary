from django.contrib import admin
from .models import Diary
# Register your models here.

@admin.register(Diary)
class UserAdmin(admin.ModelAdmin):
    pass
