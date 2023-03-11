from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required

import json

def signup(request):
    if request.POST:
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        gender = request.POST['gender']
        if password1 == password2:
            user = None
            with transaction.atomic():
                user = User.objects.create_user(email=email, username=username, password=password1)
                domain = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
                token = default_token_generator.make_token(user)
                user.send_welcomemail(domain,uid,token)
                auth_login(request,user)
        return render(request,"__02_intro/main.html")
    
    return render(request,"__01_account/signup.html")

def send_email_test(request):
    user = User.objects.get(name="김윤츙")
    print(user.email)
def activate(request,pk,token):
    pk = force_str(urlsafe_base64_decode(pk))
    user = User.objects.get(pk=pk)
    
    if user and default_token_generator.check_token(user, token): 
        user.is_active = True
        user.save()
        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('diary:intro')
    else:
        return HttpResponse('비정상적인 접근입니다.')

def login(request):
    return render(request, '__01_account/login.html')

def logout(request):
    return logout_then_login(request)


def forget_password(request):
    return render(request, '__01_account/forget_password.html')


def reset_confirm(request):
    return render(request, '__01_account/reset_confirm.html')
