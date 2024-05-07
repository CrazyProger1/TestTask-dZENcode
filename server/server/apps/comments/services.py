from django.db import models

from server.utils.django.orm import get_all_objects
from .models import Comment, CommentLike


def get_all_comments() -> models.QuerySet[Comment]:
    return get_all_objects(Comment)
