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
    MyTokenObtainPairSerializer, UserSuggestionSerializer, FollowSerializer

from accounts.validators import MyCommonPasswordValidator, MyNumericPasswordValidator, MyMinimumLengthValidator, \
    EmailNicknameValidator


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
def my_profile_fw_info(request):
    user = request.user
    serializer = UserRetrieveSerializers(user)
    return render(request,"__side_fw_info.html", {"data" : serializer.data})


@api_view(['GET'])
def my_profile_mn_info(request):
    user = request.user
    serializer = UserRetrieveSerializers(user)
    return render(request,"__side_mn_info.html", {"data" : serializer.data})

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

@api_view(['GET'])
def my_follow_list(request):
    user = request.user
    serializer = FollowSerializer(user)
    print(serializer.data)
    return render(request,"_02_main/__addon/my-flw-modal.html", {"data":serializer.data})


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


