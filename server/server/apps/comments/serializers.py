import pathlib
from functools import cache

from rest_framework import serializers, reverse

from .models import (
    Comment,
    CommentLike,
    CommentAttachment,
)
from .services import (
    count_likes,
    count_dislikes,
    get_or_create_like,
)
from .constants import (
    ALLOWED_FILE_EXTENSIONS,
    IMAGE_FILE_EXTENSIONS,
)


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("created_at", "user")

    def get_likes_count(self, comment: Comment):
        return count_likes(comment=comment)

    def get_dislikes_count(self, comment: Comment):
        return count_dislikes(comment=comment)

    def save(self, **kwargs):
        return super().save(**kwargs, user=self.context["request"].user)


class ReplyCommentSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "reply_to",
            "user",
        )

    def save(self, **kwargs):
        return super().save(**kwargs, user=self.context["request"].user)


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"
        read_only_fields = ("comment", "user")

    def create(self, validated_data):
        like = get_or_create_like(
            comment=validated_data["comment"], user=validated_data["user"]
        )
        like.positive = validated_data["positive"]
        like.save()
        return like

    def save(self, **kwargs):
        return super().save(**kwargs, user=self.context["request"].user)


class CommentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAttachment
        fields = "__all__"
        read_only_fields = (
            "type",
            "comment",
        )

    @staticmethod
    @cache
    def get_fileext(filename: str):
        return pathlib.Path(filename).suffix

    def validate_file(self, file):
        ext = self.get_fileext(file.name)
        if ext not in ALLOWED_FILE_EXTENSIONS:
            raise serializers.ValidationError(f"File extension {ext} not allowed")

        return file

    def save(self, **kwargs):
        file = self.validated_data["file"]
        ext = self.get_fileext(file.name)
        filetype = "IMG" if ext in IMAGE_FILE_EXTENSIONS else "TXT"
        return super().save(**kwargs, type=filetype)

    def to_representation(self, attachment):
        representation = super().to_representation(attachment)
        representation["file"] = self.context["request"].build_absolute_uri(reverse.reverse_lazy(
            "comment-attachments-file",
            kwargs={
                "pk": attachment.pk,
                "comment_id": attachment.comment.pk
            }
        ))
        return representation
