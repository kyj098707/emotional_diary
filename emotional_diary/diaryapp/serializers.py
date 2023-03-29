from rest_framework import serializers
from diaryapp.models import Diary,Comment

class DiaryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["id","title","content","user"]

class DiaryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        exclude = ["created_at"]

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class DiaryLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["like"]

