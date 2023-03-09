from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


def intro_test(request):
    return render(request,"__01_intro/main.html")
