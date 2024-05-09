from rest_framework import permissions

from server.apps.comments.services import get_all_likes
from server.apps.comments.serializers import CommentLikeSerializer

from server.apps.comments.views.comments import CommentParentViewSet


class CommentLikeViewSet(CommentParentViewSet):
    queryset = get_all_likes()
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(comment=self.get_parent_object())