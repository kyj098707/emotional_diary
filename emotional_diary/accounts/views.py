from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView

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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, SignupSerializer, StatsSerializer, UserRetrieveSerializers, \
    MyTokenObtainPairSerializer, UserSuggestionSerializer

from accounts.validators import MyCommonPasswordValidator, MyNumericPasswordValidator, MyMinimumLengthValidator, \
    EmailNicknameValidator

import json

User = get_user_model()


##########################
##### PAGE
##########################

def login_page(request):
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




def logout(request):
    return logout_then_login(request)


def forget_password(request):
    return render(request, '__01_account/forget_password.html')


def reset_confirm(request):
    return render(request, '__01_account/reset_confirm.html')


def statistics_test(request):
    test_data = {}
    test_data['cnt_today'] = 1512 # 오늘 방문 수
    test_data['cnt_yester'] = 15120 # 어제 방문 수
    test_data['cnt_total'] = 1120 # 누적 방문 수

    test_data['num_like'] = 1410 # 좋아요 수
    test_data['num_follower'] = 134 # 팔로우 수
    test_data['num_following'] = 1341 # 팔로우 수
    test_data['num_post'] = 1243 # 총 포스트 수

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

    return render(request,"temp_dashboard_pack/base_temp.html",{
        "data":test_data
    })


##########################
##### API
##########################

class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
@api_view(['GET'])
@permission_classes([AllowAny])
def signup_validate(request):
    """
    password validation
    - 8글자 이하, 단순, 문자 체크
    """

    email = request.GET.get('email')
    nickname = request.GET.get('nickname')
    password = request.GET.get('password')
    print(email)
    response = {"message" : "비밀번호 검증 성공", "validation" : "True"}
    en_validator = EmailNicknameValidator(email=email, nickname=nickname)
    if not en_validator.nickname_duplication():
        response["message"] = '동일한 닉네임이 존재합니다.'
        response["validation"] = "False"
    elif not en_validator.email_duplication():
        response["message"] = '동일한 이메일이 존재합니다.'
        response["validation"] = "False"
    elif not en_validator.email_format():
        response["message"] = '올바른 이메일 형식이 아닙니다.'
        response["validation"] = "False"
    elif not en_validator.nickname_format():
        response["message"] = "닉네임은 두글자 이상 적어주세요"
        response["validation"] = "False"
    elif not MyMinimumLengthValidator().validate(password):
        response["message"] = '8글자 이상의 비밀번호를 사용해주세요.'
        response["validation"] = "False"
    elif not MyCommonPasswordValidator().validate(password):
        response["message"] = '너무 단순한 비밀번호는 사용할 수 없습니다.'
        response["validation"] = "False"
    elif not MyNumericPasswordValidator().validate(password):
        response["message"] = '비밀번호에는 문자가 포함되어야 합니다'
        response["validation"] = "False"
    return Response(response)



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
def user_suggestion(request):
    current_user_id = request.user.id
    following_ids = request.user.follower.values_list('id', flat=True)
    users = User.objects.exclude(id=current_user_id).exclude(id__in=following_ids)
    users = users[:min(6,len(users))]
    serializer = UserSuggestionSerializer(users, many=True)
    return render(request,"_02_main/__addon/follow_suggestion_list.html", {"data_list" : list(serializer.data)})


@api_view(['GET'])
def my_profile_info(request):
    user = request.user
    serializer = UserRetrieveSerializers(user)
    return Response(serializer.data)

@api_view(['GET'])
def profile(request, pk):
    pass

@api_view(['GET'])
def profile_info(request, pk):
    user = get_object_or_404(User,id=pk)
    serializer = UserRetrieveSerializers(user)
    flw_message = "Follow"
    if pk in request.user.follower.values_list('id', flat=True):
        flw_message = "Following"
    data = {'flw_message': flw_message, 'data': serializer.data}
    return JsonResponse(data)

@api_view(['POST'])
def user_follow(request,pk):
    print(pk)
    following_user = get_object_or_404(User,pk=pk)
    cur_user = request.user
    if cur_user != following_user:
        if not cur_user.follower.filter(pk=pk).exists():
            cur_user.follower.add(following_user)
        else:
            cur_user.follower.remove(following_user)

    return Response(UserSuggestionSerializer(following_user).data)


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializers


@api_view(['GET'])
def my_page(request):
    user = request.user
    user_serializer = UserRetrieveSerializers(instance=user)
    return Response(user_serializer.data)


class StatsRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = StatsSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

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


