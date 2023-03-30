from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Diary,Comment,Tag
from .serializers import DiaryListSerializers,DiaryRetrieveSerializers,CommentSerializers,DiaryLikeSerializers,TagSerializers
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404,ListAPIView,RetrieveAPIView,CreateAPIView,UpdateAPIView
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

class DiaryListAPIView(ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryListSerializers

class DiaryRetrieveAPIView(RetrieveAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryRetrieveSerializers

class TagCreateAPIView(CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers

@api_view(['POST'])
def comment_create(request,pk):
    diary = get_object_or_404(Diary,pk=pk)
    comment_serializer = CommentSerializers(data=request.data)

    if comment_serializer.is_valid(raise_exception=True):
        comment_serializer.save(user=request.user,diary=diary)
        diary_serializer = DiaryRetrieveSerializers(diary)
    return Response(diary_serializer.data)

@api_view(['POST'])
def attach_tag(request,pk):
    pass


@api_view(['POST'])
def diary_like(request,pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.like.filter(pk=request.user.id).exists():
        diary.like.remove(request.user) 
    else:
        diary.like.add(request.user)
    serializer = DiaryLikeSerializers(diary)
    return Response(serializer.data)



## 개인 블로그 페이지
def personal(request):
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

