import pathlib
from functools import cache

from rest_framework import serializers, reverse

from server.apps.comments.models import CommentAttachment
from server.apps.comments.constants import (
    ALLOWED_FILE_EXTENSIONS,
    IMAGE_FILE_EXTENSIONS,
)


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
        representation["file"] = self.context["request"].build_absolute_uri(
            reverse.reverse_lazy(
                "comment-attachments-file",
                kwargs={"pk": attachment.pk, "comment_id": attachment.comment.pk},
            )
        )
        return representation
