from django.contrib import admin

from server.apps.comments.models import (
    Comment,
    CommentLike,
    CommentAttachment,
)

admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(CommentAttachment)
