from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Diary, Like_user_diary, Re_diary_tag, Comment,Tag
from accounts.models import Follower,Following
from .serializers import DiarySerializers
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import status
# Create your views here.


def intro_test(request):
    qs = Diary.objects.all()
    return render(request,"__02_intro/main.html",{
        "diary_list":qs
    })

def intro_test2(request):
    diary_qs = Diary.objects.all()
    user_qs = User.objects.all()
    return render(request,"__test/main.html",{
        "diary_list":diary_qs,
        "user_list":user_qs
    })

def profile_test(request,pk):
    if User.objects.filter(pk=pk).exists():
        user = User.objects.get(pk=pk)
        diary_list = Diary.objects.filter(user=user)
        return render(request,"__01_account/profile.html",{
            "user":User.objects.get(pk=pk),
            "diary_list":diary_list
        })        
    return 

@login_required
def diary_new(request):
    pass

### diary로 옮기기
@api_view(['POST'])
def user_follow(request):
    username = request.POST.get("username")
    fan = get_object_or_404(User,username=username)
    celeb = request.user
    with transaction.atomic():        
        Following.objects.create(user=fan, following=celeb)
        Follower.objects.create(user=celeb,follower=fan)
    return Response(status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def user_unfollow(request):
    username = request.POST.get("username")
    fan = get_object_or_404(User,username=username)
    celeb = request.user
    with transaction.atomic(): 
        Following.objects.get(user=fan, following=celeb).delete()
        Follower.objects.get(user=celeb,follower=fan).delete()
    return Response(status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def user_like(request):
    diary_name = request.POST.get("diary_name")
    diary = get_object_or_404(diary_name)
    user = request.user
    Like_user_diary.objects.create(user=user, diary=diary,like=True)
    return Response(status.HTTP_204_NO_CONTENT)

### db 관리
class DiaryViewSet(ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializers
    permission_classes = [AllowAny]

## 개인 블로그 페이지
def personal(request):
    return render(request, "__03_personal/personal_blog.html")

