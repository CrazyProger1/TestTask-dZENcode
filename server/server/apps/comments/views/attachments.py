from django.http import FileResponse

from rest_framework import (
    permissions,
    decorators,
)

from server.apps.comments.services import (
    get_all_attachments,
    get_comment_attachments,
    mark_comment_has_attachment,
)
from server.apps.comments.serializers import CommentAttachmentSerializer
from server.apps.comments.permissions import CanAddAttachments
from server.apps.comments.views.comments import CommentParentViewSet


class CommentAttachmentViewSet(CommentParentViewSet):
    queryset = get_all_attachments()
    serializer_class = CommentAttachmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CanAddAttachments)

    def perform_create(self, serializer):
        comment = self.get_parent_object_or_404()
        mark_comment_has_attachment(comment=comment)
        serializer.save(comment=comment)

    def get_queryset(self):
        comment = self.get_parent_object()
        if comment:
            return get_comment_attachments(comment=comment)
        return self.queryset

    @decorators.action(detail=True, methods=["get"])
    def file(self, request, comment_id: int, pk: int):
        attachment = self.get_object()
        return FileResponse(open(attachment.file.name, "rb"), as_attachment=True)
