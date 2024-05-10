from rest_framework import serializers

from server.apps.comments.models import Comment
from server.apps.comments.services import count_likes, count_dislikes


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("created_at", "user", "has_attachment")

    def get_likes_count(self, comment: Comment):
        return count_likes(comment=comment)

    def get_dislikes_count(self, comment: Comment):
        return count_dislikes(comment=comment)

    def save(self, **kwargs):
        user = kwargs.pop("user", None)
        if not user:
            user = self.context["request"].user
        return super().save(**kwargs, user=user)
