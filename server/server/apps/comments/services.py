from django.db import models
from django.shortcuts import get_object_or_404

from server.utils.django.orm import get_all_objects
from .models import (
    Comment,
    CommentLike,
    CommentAttachment,
)


def count_likes(comment: Comment):
    return comment.likes.filter(positive=True).count()


def count_dislikes(comment: Comment):
    return comment.likes.filter(positive=False).count()


def get_or_create_like(**data) -> CommentLike:
    return CommentLike.objects.get_or_create(**data)[0]


def get_all_likes() -> models.QuerySet[CommentLike]:
    return get_all_objects(CommentLike)


def get_all_comments() -> models.QuerySet[Comment]:
    return get_all_objects(Comment)


def get_all_attachments() -> models.QuerySet[CommentAttachment]:
    return get_all_objects(CommentAttachment)


def get_comment_attachments(comment: Comment) -> models.QuerySet[CommentAttachment]:
    return comment.attachments.all()


def get_parent_comments() -> models.QuerySet[Comment]:
    return Comment.objects.filter(reply_to__isnull=True)


def get_reply_comments() -> models.QuerySet[Comment]:
    return Comment.objects.filter(reply_to__isnull=False)


def get_comment_replies(comment: Comment) -> models.QuerySet[Comment]:
    return comment.replies.all()


def get_comment_or_none(**filters) -> Comment | None:
    try:
        return Comment.objects.get(**filters)
    except Comment.DoesNotExist:
        return None


def get_comment_or_404(**filters) -> Comment:
    return get_object_or_404(Comment, **filters)


def get_comment_likes(comment: Comment) -> models.QuerySet[CommentLike]:
    return CommentLike.objects.filter(comment=comment)


def mark_comment_has_attachment(comment: Comment):
    if not comment.has_attachment:
        comment.has_attachment = True
        comment.save()
