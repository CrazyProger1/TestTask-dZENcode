import pathlib
from functools import cache

from rest_framework import serializers

from .models import Comment, CommentLike, CommentAttachment
from .services import count_likes, count_dislikes
from .constants import ALLOWED_FILE_EXTENSIONS, IMAGE_FILE_EXTENSIONS, TEXT_FILE_EXTENSIONS


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


class ReplyCommentSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "reply_to",
        )


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"


class CommentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAttachment
        fields = "__all__"
        read_only_fields = ("type", "comment",)

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
