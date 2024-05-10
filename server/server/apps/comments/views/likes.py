from django.http import Http404
from rest_framework import permissions

from server.apps.comments.services import get_all_likes, get_comment_likes
from server.apps.comments.serializers import CommentLikeSerializer

from server.apps.comments.views.comments import CommentParentViewSet


class CommentLikeViewSet(CommentParentViewSet):
    queryset = get_all_likes()
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        comment = self.get_parent_object()
        if comment:
            return get_comment_likes(comment=comment)
        return self.queryset

    def perform_create(self, serializer):
        comment = self.get_parent_object_or_404()
        serializer.save(comment=comment)
