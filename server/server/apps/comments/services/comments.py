from django.db import models
from django.shortcuts import get_object_or_404

from server.apps.comments.models import Comment
from server.utils.django.orm import get_all_objects, get_object_or_none


def get_all_comments() -> models.QuerySet[Comment]:
    return get_all_objects(Comment)


def mark_comment_has_attachment(comment: Comment):
    if not comment.has_attachment:
        comment.has_attachment = True
        comment.save()


def get_comment_or_404(**filters) -> Comment:
    return get_object_or_404(Comment, **filters)


def get_comment_or_none(**filters) -> Comment | None:
    return get_object_or_none(Comment, **filters)
