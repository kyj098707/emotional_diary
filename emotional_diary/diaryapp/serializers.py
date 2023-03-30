from rest_framework import serializers
from accounts.serializers import UserSerializer
from diaryapp.models import Diary,Comment

class DiaryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["id","title","content","user"]

class DiaryRetrieveSerializers(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Diary
        fields = "__all__"

    def get_comment(self, diary):
        comment = Comment.objects.filter(diary=diary)
        serializers = CommentSerializers(instance=comment,many=True)
        return serializers.data

class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    diary = DiaryListSerializers(required=False)
    class Meta:
        model = Comment
        fields = "__all__"


class DiaryLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["like"]

