from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from diaryapp.models import Diary

User = get_user_model()


class DiaryEmotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["happiness","angry","disgust","fear","neutral","sadness","surprise"]

class UserSuggestionSerializer(serializers.ModelSerializer):
    num_following = serializers.SerializerMethodField()
    num_follower = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "num_following", "num_follower"]

    def get_num_following(self,user):
        return user.follower.count()

    def get_num_follower(self,user):
        user = User.objects.filter(follower=user)
        return len(user)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# Like 개수, Follower 수, Posting 수, 감정 추이
# 나중에 리펙토링
class StatsSerializer(serializers.ModelSerializer):
    num_like = serializers.SerializerMethodField()
    num_posting = serializers.SerializerMethodField()
    num_follower = serializers.SerializerMethodField()
    emotional_trend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id","username","nickname","follower","num_like","num_posting","num_follower","emotional_trend"]

    def get_num_like(self,obj):
        diary_list = Diary.objects.filter(user=obj)
        total_like = 0 if diary_list is None else sum([diary.like.count() for diary in diary_list])
        return total_like

    def get_num_posting(self,obj):
        diary_list = Diary.objects.filter(user=obj)
        return len(diary_list)

    def get_num_follower(self,obj):
        return obj.follower.count()

    def get_emotional_trend(self,obj):
        diary_list = Diary.objects.filter(user=obj)
        emotion_serializer = DiaryEmotionSerializers(instance=diary_list,many=True)
        return emotion_serializer.data


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
        #self.send_mail(validated_data["email"])
        return user

    class Meta:
        model = User
        fields = ['pk','email','username','password']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = {}
        try:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['email'] = self.user.email
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            if self.user.is_active == False:
                data['response'] = 'activate_error'
            else:
                data['response'] = 'complete'
        except Exception as e:
            data['response'] = 'error'
        return data
