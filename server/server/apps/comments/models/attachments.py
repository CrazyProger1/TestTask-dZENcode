from django.db import models

from server.apps.comments.models import Comment


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
