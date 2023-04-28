import torch
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse
from rest_framework.response import Response
from transformers import AutoTokenizer

from .models import Diary,Comment,Tag
from .serializers import DiaryListSerializers, DiaryRetrieveSerializers, CommentSerializers, DiaryLikeNumSerializers, \
    TagSerializers, DiaryCreateSerializers
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView


######
## API
######

@api_view(['GET'])
def profile_info(request, pk):
    follow_message = "Follow"
    user = get_object_or_404(User, id=pk)
    print(request.user)
    if pk in request.user.follower.values_list('id', flat=True):
        follow_message = "Following"
    return Response({"data": pk, "follow_message": follow_message})


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
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizers = AutoTokenizer.from_pretrained("klue/roberta-small")
        model = torch.load("./best_roberta_model.pt", map_location=torch.device(device))
        create_serializer = DiaryCreateSerializers(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        obj = create_serializer.save(user=request.user)
        for tag_name in request.data["tags"]:
            tag_name = tag_name[1:] # #제거
            if not Tag.objects.filter(name=tag_name).exists():
                Tag.objects.create(name=tag_name)
            obj.tag.add(Tag.objects.get(name=tag_name))

        input_tokens = tokenizers(request.data["content"], return_tensors='pt')
        attention_mask = input_tokens['attention_mask'].to(device)
        input_ids = input_tokens['input_ids'].squeeze(1).to(device)
        fear_output, disgust_output, surprise_output, happiness_output, sadness_output, angry_output = model(input_ids,
                                                                                              attention_mask)
        obj.fear = fear_output.item()
        obj.disgust = disgust_output.item()
        obj.surprise = surprise_output.item()
        obj.happiness = happiness_output.item()
        obj.sadness = sadness_output.item()
        obj.angry = angry_output.item()
        obj.save()
        diary = Diary.objects.filter(user=request.user).order_by("-created_at")
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


    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return render(request, "_02_main/__addon/center_post_list.html", {"data": list(serializer.data)})


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


