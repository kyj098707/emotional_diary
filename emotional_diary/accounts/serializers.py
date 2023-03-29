from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_str


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def send_mail(self,email):
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        token = default_token_generator.make_token(user)
        user.send_welcomemail(uid,token)

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"],
                                username=validated_data["username"],
                                password=validated_data["password"])
        self.send_mail(validated_data["email"])
        return user

    class Meta:
        model = User
        fields = ['pk','email','username','password']