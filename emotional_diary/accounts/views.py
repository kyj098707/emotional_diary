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
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, SignupSerializer

import json

User = get_user_model()

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

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def login(request):
    if request.POST:
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
    return render(request, '__01_account/login.html')

def logout(request):
    return logout_then_login(request)


def forget_password(request):
    return render(request, '__01_account/forget_password.html')


def reset_confirm(request):
    return render(request, '__01_account/reset_confirm.html')


def statistics_test(request):
    test_data = {}
    test_data['cnt_today'] = 7 # 오늘 방문 수
    test_data['cnt_yester'] = 10 # 어제 방문 수
    test_data['cnt_total'] = 10 # 누적 방문 수

    test_data['num_like'] = 10 # 좋아요 수
    test_data['num_follow'] = 13 # 팔로우 수

    # 감정 반환 API 필요,
    # 수치순으로 반환 + 각 감정 라벨링할것인지
    # 감정 순서는 고정, 수치로만 반환할지 등
    # 비율이 아닌 수치로 맵할지 몰라서 일단 수치로 테스트했어요.

    test_feels = [25, 17, 31, 46, 11]
    test_data['total_feel'] = sum(test_feels)
    test_data['feel1'] = test_feels[0]
    test_data['feel2'] = test_feels[1]
    test_data['feel3'] = test_feels[2]
    test_data['feel4'] = test_feels[3]
    test_data['feel5'] = test_feels[4]

    return render(request,"__01_account/statistics.html",{
        "data":test_data
    })

## restapi_framework test

class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]

@api_view(['GET'])
def email_validate(request):
    ## 유저 이메일 중복 체크
    email = request.GET.get("email")
    try:
        if User.objects.get(email=email):
            result = {'response':'complete'}
    except:
        result = {'response':'email_valid_fail'}
    return HttpResponse(result, content_type="application/json")

@api_view(['GET'])
def email_validate(request):
    ## 유저 이메일 중복 체크
    email = request.GET.get("email")
    try:
        if User.objects.get(email=email):
            result = {'response':'complete'}
    except:
        result = {'response':'email_valid_fail'}
    return HttpResponse(result, content_type="application/json")

"""
@api_view(['GET'])
def login(request):
    email = request.GET.get("email")
    password = request.GET.get("email")
    user = authenticate(email,password)
    if user :
        auth_login(request,user)
        result = {'response':'complete'}
    else:
        result = {'response':'fail'}
    return HttpResponse(result, content_type="application/json")
"""


