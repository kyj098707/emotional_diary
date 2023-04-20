from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
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
    MyTokenObtainPairSerializer

from accounts.validators import MyCommonPasswordValidator, MyNumericPasswordValidator, MyMinimumLengthValidator, \
    EmailNicknameValidator

import json

def login(request):
    return render(request, '_01_account/login.html')