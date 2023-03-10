from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User
from django.db import transaction

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
                user = User.objects.create_user(email=email, username=username, password=password1)
                user.send_welcomemail()
        return render(request,"__02_intro/main.html")
    
    return render(request,"__01_account/signup.html")