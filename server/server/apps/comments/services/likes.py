from django.db import models

from server.apps.comments.models import CommentLike, Comment
from server.utils.django.orm import get_all_objects, get_or_create_object


def get_or_create_like(**data) -> CommentLike:
    return get_or_create_object(CommentLike, **data)


def get_all_likes() -> models.QuerySet[CommentLike]:
    return get_all_objects(CommentLike)


def count_likes(comment: Comment):
    return comment.likes.filter(positive=True).count()


def count_dislikes(comment: Comment):
    return comment.likes.filter(positive=False).count()


def get_comment_likes(comment: Comment) -> models.QuerySet[CommentLike]:
    return CommentLike.objects.filter(comment=comment)
