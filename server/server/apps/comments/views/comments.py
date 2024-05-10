from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    permissions,
    filters,
)

from server.apps.comments.filters import CommentFilter
from server.apps.comments.models import Comment
from server.apps.comments.serializers import CommentSerializer
from server.apps.comments.services import (
    get_all_comments,
    get_parent_comments,
    get_comment_or_none,
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = get_all_comments()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at",)
    ordering = "-created_at"
    filterset_class = CommentFilter

    def get_queryset(self):
        if self.action == "list":
            return get_parent_comments()
        return self.queryset


class CommentParentViewSet(viewsets.ModelViewSet):
    def get_parent_object(self) -> Comment | None:
        pk = self.kwargs.get("comment_id")
        return get_comment_or_none(pk=pk)

    def get_parent_object_or_404(self) -> Comment:
        comment = self.get_parent_object()
        if not comment:
            raise Http404("Parent comment not found")
        return comment
