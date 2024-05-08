from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    viewsets,
    permissions,
    decorators,
    response,
    request,
    exceptions,
    filters,
)

from .services import (
    get_comment_replies,
    get_all_likes,
    get_parent_comments,
    get_reply_comments,
    get_comment_or_none,
    get_all_comments,
)
from .serializers import (
    CommentSerializer,
    CommentLikeSerializer,
    ReplyCommentSerializer,
)
from .constants import COMMENT_PAGE_SIZE
from .permissions import IsCommentOwnerOrReadOnly
from .filters import CommentFilter


class CommentViewSet(viewsets.ModelViewSet):
    queryset = get_all_comments()
    serializer_class = CommentSerializer
    page_size = COMMENT_PAGE_SIZE
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = [
        "created_at",
    ]
    filterset_class = CommentFilter

    def get_queryset(self):
        if self.action == "list":
            return get_parent_comments()
        return self.queryset


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = get_reply_comments()
    serializer_class = ReplyCommentSerializer
    page_size = COMMENT_PAGE_SIZE
    permission_classes = (permissions.IsAuthenticated, IsCommentOwnerOrReadOnly)

    def get_parent_object(self):
        pk = self.kwargs.get("comment_id")
        return get_comment_or_none(pk=pk)

    def perform_create(self, serializer):
        serializer.save(reply_to=self.get_parent_object())

    def get_queryset(self):
        comment = self.get_parent_object()

        if not comment:
            raise exceptions.NotFound(detail="Parent comment not found")

        return get_comment_replies(comment=comment)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = get_all_likes()
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticated, IsCommentOwnerOrReadOnly)
