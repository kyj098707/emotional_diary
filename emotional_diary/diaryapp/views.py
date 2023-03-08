from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Diary

# Create your views here.


@login_required
def profile(request):
    return render(request,"__01_account/profile.html")
"""
def diary_list(request):
    qs = Diary.objects.all()

def my_diary(request, pk)
"""