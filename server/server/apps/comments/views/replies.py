from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    permissions,
    filters,
)

from server.apps.comments.serializers import ReplyCommentSerializer
from server.apps.comments.permissions import IsCommentOwnerOrReadOnly
from server.apps.comments.filters import CommentFilter
from server.apps.comments.services import (
    get_comment_replies,
    get_reply_comments,
)
from server.apps.comments.views.comments import CommentParentViewSet


class ReplyViewSet(CommentParentViewSet):
    queryset = get_reply_comments()
    serializer_class = ReplyCommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsCommentOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at",)
    ordering = "-created_at"
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        serializer.save(reply_to=self.get_parent_object())

    def get_queryset(self):
        comment = self.get_parent_object()
        return get_comment_replies(comment=comment)
