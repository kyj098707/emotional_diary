from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from .models import User
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required

import json



##########################
##### PAGE
##########################

def login(request):
    """if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not User.objects.filter(email=email).exists():
            return HttpResponse('등록되지 않은 이메일입니다.')

        user = User.objects.get(email=email)
        ## 아이디가 비활성화 일 때
        if not user.is_active:
            return render(request,'__00_exception/non_activate_accounts.html')

        ## 활성된 아이디일 경우
        user = authenticate(email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect('diary:intro')
        return HttpResponse('아이디와 비밀번호가 틀렸습니다.')
    """
    return render(request, '_01_account/login.html')


def activate(request,pk,token):
    print("A")
    pk = force_str(urlsafe_base64_decode(pk))
    User = get_user_model()
    user = User.objects.get(pk=pk)
    if user and default_token_generator.check_token(user, token): 
        user.is_active = True
        user.save()
        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('diary:intro')
    else:
        return HttpResponse('비정상적인 접근입니다.')



def logout(request):
    return logout_then_login(request)