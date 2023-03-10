from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User
from django.db import transaction
from django.contrib.auth import authenticate, login

import json

def signup(request):
    if request.POST:
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        gender = request.POST['gender']
        if password1 == password2:
            with transaction.atomic():
                User.objects.create_user(email=email, username=username, password=password1)

        return render(request,"__02_intro/main.html")
    
    return render(request,"__01_account/signup.html")


def login(request):
    return render(request, '__01_account/login.html')


def forget_password(request):
    return render(request, '__01_account/forget_password.html')


def reset_confirm(request):
    return render(request, '__01_account/reset_confirm.html')
