from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Diary,Comment,Tag
from .serializers import DiaryListSerializers,DiaryRetrieveSerializers,CommentSerializers,DiaryLikeNumSerializers,TagSerializers
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView


################
## PAGE
################

def newsfeed_list(request):
    diary_qs = Diary.objects.all()
    serializer = DiaryListSerializers(diary_qs,many=True)
    return render(request,"__02_intro/detail_diary_test.html", {"data" : list(serializer.data)})


def newsfeed_test(request,pk):
    diary = get_object_or_404(Diary, pk=pk)
    serializer = DiaryRetrieveSerializers(diary)
    return render(request, "__02_intro/detail_diary_test.html",{
        "data": serializer.data,
    })


def personal_page(request):
    '''posts : PostModel.objects.all()
    if request.method == 'POST' :
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = reqeust.user
            instance.save()
            return redirect('personal_blog')

    else :
        form = PostModelForm()
    form = PostModelForm()
    context = {
        'post' : posts,
        'form' : form
    }'''
    return render(request, "__03_personal/personal_blog.html")


def intro_test(request):
    # return render(request, "__02_intro/intro_test.html")
    return render(request, "base_layout.html")

def profile_test(request,pk):
    user = get_object_or_404(User,id=pk)
    return render(request, "_02_main/profile_page.html", {
        "data": pk,
    })

## 개인 블로그 페이지



## main

def home(request):
    return render(request, "_02_main/_00_home/home.html")

def post(request):
    return render(request, "_02_main/_01_post/my post.html")


def social(request):
    return render(request, "base_layout.html")
