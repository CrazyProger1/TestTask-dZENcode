from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    viewsets,
    permissions,
    filters,
    decorators,
    response,
)

from .services import (
    get_comment_replies,
    get_all_likes,
    get_parent_comments,
    get_reply_comments,
    get_comment_or_404,
    get_all_comments,
    get_all_attachments,
    get_comment_attachments,
)
from .serializers import (
    CommentSerializer,
    CommentLikeSerializer,
    ReplyCommentSerializer,
    CommentAttachmentSerializer,
)
from .constants import COMMENT_PAGE_SIZE
from .permissions import IsCommentOwnerOrReadOnly, CanAddAttachments
from .filters import CommentFilter


class CommentViewSet(viewsets.ModelViewSet):
    queryset = get_all_comments()
    serializer_class = CommentSerializer
    page_size = COMMENT_PAGE_SIZE
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at",)
    ordering = "-created_at"
    filterset_class = CommentFilter

    def get_queryset(self):
        if self.action == "list":
            return get_parent_comments()
        return self.queryset


class CommentParentViewSet(viewsets.ModelViewSet):
    def get_parent_object(self):
        pk = self.kwargs.get("comment_id")
        return get_comment_or_404(pk=pk)


class ReplyViewSet(CommentParentViewSet):
    queryset = get_reply_comments()
    serializer_class = ReplyCommentSerializer
    page_size = COMMENT_PAGE_SIZE
    permission_classes = (permissions.IsAuthenticated, IsCommentOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at",)
    ordering = "-created_at"
    filterset_class = CommentFilter

    def get_parent_object(self):
        pk = self.kwargs.get("comment_id")
        return get_comment_or_404(pk=pk)

    def perform_create(self, serializer):
        serializer.save(reply_to=self.get_parent_object())

    def get_queryset(self):
        comment = self.get_parent_object()
        return get_comment_replies(comment=comment)


class CommentLikeViewSet(CommentParentViewSet):
    queryset = get_all_likes()
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(comment=self.get_parent_object())


class CommentAttachmentViewSet(CommentParentViewSet):
    queryset = get_all_attachments()
    serializer_class = CommentAttachmentSerializer
    permission_classes = (permissions.IsAuthenticated, CanAddAttachments)

    def perform_create(self, serializer):
        serializer.save(comment=self.get_parent_object())

    def get_queryset(self):
        comment = self.get_parent_object()
        return get_comment_attachments(comment=comment)

    @decorators.action(detail=True, methods=['get'])
    def file(self, request, comment_id: int, pk: int):
        attachment = self.get_object()
        return FileResponse(open(attachment.file.name, 'rb'), as_attachment=True)
