from rest_framework import serializers

from server.apps.comments.models import CommentLike
from server.apps.comments.services import get_or_create_like


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"
        read_only_fields = ("comment", "user")

    def create(self, validated_data):
        like = get_or_create_like(
            comment=validated_data["comment"],
            user=validated_data["user"],
        )
        like.positive = validated_data["positive"]
        like.save()
        return like

    def save(self, **kwargs):
        return super().save(**kwargs, user=self.context["request"].user)
