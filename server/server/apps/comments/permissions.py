from rest_framework import permissions

from .services import get_comment_or_404


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class CanAddAttachments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            comment_id = view.kwargs['comment_id']
            comment = get_comment_or_404(pk=comment_id)
            return comment.user == request.user

        return True
