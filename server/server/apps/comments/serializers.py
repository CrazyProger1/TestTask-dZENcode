from rest_framework import serializers

from .models import Comment, CommentLike
from .services import count_likes, count_dislikes


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("created_at",)

    def get_likes_count(self, comment: Comment):
        return count_likes(comment=comment)

    def get_dislikes_count(self, comment: Comment):
        return count_dislikes(comment=comment)


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"
