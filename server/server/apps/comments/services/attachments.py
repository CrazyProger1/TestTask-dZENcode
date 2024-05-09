from django.db import models

from server.apps.comments.models import CommentAttachment, Comment
from server.utils.django.orm import get_all_objects


def get_all_attachments() -> models.QuerySet[CommentAttachment]:
    return get_all_objects(CommentAttachment)


def get_comment_attachments(comment: Comment) -> models.QuerySet[CommentAttachment]:
    return comment.attachments.all()
