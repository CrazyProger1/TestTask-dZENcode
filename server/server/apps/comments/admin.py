from django.contrib import admin

from .models import Comment, CommentLike

admin.site.register(Comment)
admin.site.register(CommentLike)
