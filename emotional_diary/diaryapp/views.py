from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Diary, Like, Re_diary_tag, Comment,Tag
from accounts.models import Follower,Following
from .serializers import DiarySerializers
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
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
    uid = request.POST.get("id")
    fan = get_object_or_404(User,pk=uid)
    celeb = request.user
    with transaction.atomic():
        if not Following.objects.filter(user=fan, following=celeb).exists() and fan != celeb:
            Following.objects.create(user=fan, following=celeb)
            Follower.objects.create(user=celeb,follower=fan)
    return Response(status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def user_unfollow(request):
    uid = request.POST.get("id")
    fan = get_object_or_404(User,pk=uid)
    celeb = request.user
    with transaction.atomic():
        if Following.objects.filter(user=fan, following=celeb).exists():  
            Following.objects.get(user=fan, following=celeb).delete()
            Follower.objects.get(user=celeb,follower=fan).delete()
    return Response(status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def diary_like(request):
    print("11")
    diary_id = request.POST.get("diary_id")
    diary = get_object_or_404(Diary,pk=diary_id)
    user = request.user
    if not Like.objects.filter(user=user, diary=diary):
        Like.objects.create(user=user, diary=diary)
    return Response(status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def diary_dislike(request):
    diary_id = request.POST.get("diary_id")
    diary = get_object_or_404(Diary,pk=diary_id)
    user = request.user
    if Like.objects.filter(user=user, diary=diary):
        Like.objects.get(user=user, diary=diary).delete()
    return Response(status.HTTP_204_NO_CONTENT)



class DiaryDetailAPIView(APIView):
    pass

## 개인 블로그 페이지
def personal(request):
    return render(request, "__03_personal/personal_blog.html")

