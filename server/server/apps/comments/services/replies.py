from django.db import models

from server.apps.comments.models import Comment


def get_parent_comments() -> models.QuerySet[Comment]:
    return Comment.objects.filter(reply_to__isnull=True)


def get_reply_comments() -> models.QuerySet[Comment]:
    return Comment.objects.filter(reply_to__isnull=False)


def get_comment_replies(comment: Comment) -> models.QuerySet[Comment]:
    return comment.replies.all()
