from rest_framework import serializers
from accounts.serializers import UserSerializer
from diaryapp.models import Diary,Comment,Tag


class DiaryLikeNumSerializers(serializers.ModelSerializer):
    num_like = serializers.SerializerMethodField()

    class Meta:
        model = Diary
        fields = ["num_like"]

    def get_num_like(self, diary):
        return diary.like.count()




class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class DiaryCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["title","content"]


class DiaryListSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    num_like = serializers.SerializerMethodField()
    num_comment = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    emotion = serializers.SerializerMethodField()
    tag = TagSerializers(many=True)

    class Meta:
        model = Diary
        fields = ["id","title","content","user","num_like", "num_comment","created_at","comment","tag","emotion"]

    def get_num_comment(self, diary):
        comment_list = Comment.objects.filter(diary=diary)
        return len(comment_list)
    def get_num_like(self, diary):
        return diary.like.count()

    def get_comment(self, diary):
        comment = Comment.objects.filter(diary=diary).order_by("-created_at")
        serializers = DiaryCommentSerializers(instance=comment, many=True)
        return serializers.data

    def get_emotion(self,diary):
        emoji = {"fear":"😖","disgust":"🤐","surprise":"😵","happiness":"😊","sadness":"😥","angry":"😡","neutral":"😶"}
        emotion = sorted([(diary.fear, "fear"), (diary.disgust, "disgust"), (diary.surprise, "surprise"), \
                          (diary.happiness, "happiness"), (diary.sadness, "sadness"), (diary.angry, "angry")],
                         reverse=True)
        print(emotion)
        emotion = emotion[0][1] if emotion[0][0] > 0.5 else "neutral"
        return {"emoji":emoji[emotion], "emotion":emotion}

class DiaryRetrieveSerializers(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    tag = TagSerializers(many=True)
    num_like = serializers.SerializerMethodField()
    num_comment = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Diary
        fields = "__all__"

    def get_comment(self, diary):
        comment = Comment.objects.filter(diary=diary).order_by("-created_at")
        serializers = DiaryCommentSerializers(instance=comment,many=True)
        return serializers.data
    def get_num_comment(self, diary):
        comment_list = Comment.objects.filter(diary=diary)
        return len(comment_list)
    def get_num_like(self, diary):
        return diary.like.count()




class DiaryCommentSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ["id","user","content","created_at"]




class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    diary = DiaryListSerializers(required=False)
    class Meta:
        model = Comment
        fields = "__all__"

