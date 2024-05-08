from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
    )
    has_attachment = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    positive = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ("user", "comment")


class CommentAttachment(models.Model):
    TYPES = (
        ("TXT", "Text File"),
        ("IMG", "Image File"),
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(upload_to="files/attachments/")
    type = models.CharField(max_length=3, choices=TYPES)

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
