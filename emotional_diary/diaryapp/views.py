from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Diary
from .serializers import DiarySerializers
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
# Create your views here.


def intro_test(request):
    qs = Diary.objects.all()
    return render(request,"__02_intro/main.html",{
        "diary_list":qs
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

### db 관리
class DiaryViewSet(ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializers


## 개인 블로그 페이지
def personal(request):
    return render(request, "__03_personal/personal_blog.html")
