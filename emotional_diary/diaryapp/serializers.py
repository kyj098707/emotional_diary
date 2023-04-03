from rest_framework import serializers
from accounts.serializers import UserSerializer
from diaryapp.models import Diary,Comment,Tag

class DiaryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["id","title","content","user"]


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]




class DiaryRetrieveSerializers(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    tag = TagSerializers(many=True)

    class Meta:
        model = Diary
        fields = "__all__"

    def get_comment(self, diary):
        comment = Comment.objects.filter(diary=diary).order_by("-created_at")
        serializers = DiaryCommentSerializers(instance=comment,many=True)
        return serializers.data



class DiaryCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","user","content","created_at"]

class DiaryLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["like"]

class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    diary = DiaryListSerializers(required=False)
    class Meta:
        model = Comment
        fields = "__all__"

