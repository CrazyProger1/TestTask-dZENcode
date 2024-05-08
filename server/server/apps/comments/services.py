from django.db import models

from server.utils.django.orm import get_all_objects
from .models import Comment, CommentLike


def count_likes(comment: Comment):
    return comment.likes.filter(positive=True).count()


def count_dislikes(comment: Comment):
    return comment.likes.filter(positive=False).count()


def get_all_likes() -> models.QuerySet[CommentLike]:
    return get_all_objects(CommentLike)


def get_all_comments() -> models.QuerySet[Comment]:
    return get_all_objects(Comment)


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


def get_comment_likes(comment: Comment) -> models.QuerySet[CommentLike]:
    return CommentLike.objects.filter(comment=comment)
