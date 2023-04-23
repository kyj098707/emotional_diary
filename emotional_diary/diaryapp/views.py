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





def intro_test2(request):
    diary_qs = Diary.objects.all()
    return render(request,"__02_intro/main.html",{
        "diary_list":diary_qs,
    })

def layout_test(request):
    # return render(request, "temp_dashboard_pack/base_temp.html")
    # return render(request, "base_layout.html")
    # return render(request, "_01_account/login.html")
    return render(request, "_02_main/my post.html")
    

def profile_test(request,pk):
    user = get_object_or_404(User,id=pk)
    return render(request, "_02_main/profile_page.html", {
        "data": pk,
    })

@api_view(['GET'])
def profile_info(request,pk):
    follow_message = "Follow"
    user = get_object_or_404(User, id=pk)
    print(request.user)
    if pk in request.user.follower.values_list('id', flat=True):
        follow_message = "Following"
    return Response({"data":pk,"follow_message":follow_message})
######
## API
######


@api_view(['GET'])
def my_diary_list(request):
    queryset = Diary.objects.filter(user=request.user).order_by("-created_at")
    serializer_class = DiaryListSerializers

    serializer = serializer_class(queryset, many=True)
    return render(request, "_02_main/__addon/center_post_list.html", {"data": list(serializer.data)})

@api_view(['GET'])
def user_diary_list(request,pk):
    print(pk)
    user = get_object_or_404(User,id=pk)
    queryset = Diary.objects.filter(user=user).order_by("-created_at")
    serializer_class = DiaryListSerializers

    serializer = serializer_class(queryset, many=True)
    return render(request, "_02_main/__addon/center_post_list.html", {"data": list(serializer.data)})


class DiaryListCreateAPIView(ListCreateAPIView):
    queryset = Diary.objects.order_by("-created_at")
    serializer_class = DiaryListSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=request.user)
        for tag_name in request.data["tags"]:
            tag_name = tag_name[1:] # #제거
            if not Tag.objects.filter(name=tag_name).exists():
                Tag.objects.create(name=tag_name)
            obj.tag.add(Tag.objects.get(name=tag_name))
        diary = Diary.objects.filter(user=request.user)
        serializer = self.get_serializer(diary, many=True)

        return render(request,"_02_main/__addon/center_post_list.html", {"data" : list(serializer.data)})

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return render(request,"_02_main/__addon/center_post_list.html", {"data" : list(serializer.data)})


class DiaryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiaryRetrieveSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return render(request,"_02_main/__addon/follow_suggestion_list.html", {"data" : list(serializer.data)})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = Diary.objects.order_by("-created_at")
        serializer = DiaryListSerializers(queryset,many=True)
        return render(request,"_02_main/__addon/center_post_list.html", {"data" : list(serializer.data)})

class TagListCreateAPIView(ListCreateAPIView):
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
    diary = get_object_or_404(Diary,pk=pk)
    tag = get_object_or_404(Tag,name=request.data["name"])
    print(tag.name)
    if not diary.tag.filter(name=tag.name).exists():
        print(tag.name)
        diary.tag.add(tag)
    return HttpResponse(status=200)

        


@api_view(['POST'])
def diary_like(request,pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.like.filter(pk=request.user.id).exists():
        diary.like.remove(request.user) 
    else:
        diary.like.add(request.user)
    serializer = DiaryLikeNumSerializers(diary)
    return Response(serializer.data)


## 개인 블로그 페이지



def diary_create(request):

    return render(request, "__03_personal/diary_create.html")

def diary_edit(request):

    return render(request, "__03_personal/diary_edit.html")


def diary_delete(request):

    return render(request, "__03_personal/diary_delete.html")


def diary_comment(request):

    return render(request, "__03_personal/diary_comment.html")


