from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Diary
# Create your views here.


def intro_test(request):
    qs = Diary.objects.all()
    return render(request,"__02_intro/main.html",{
        "diary_list":qs
    })
