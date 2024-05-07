from rest_framework import (
    viewsets,
    permissions,
    decorators,
    response,
    request,
)

from .services import get_all_comments, get_comment_replies
from .serializers import CommentSerializer
from .constants import COMMENT_PAGE_SIZE


class CommentViewSet(viewsets.ModelViewSet):
    queryset = get_all_comments()
    serializer_class = CommentSerializer
    page_size = COMMENT_PAGE_SIZE
    permission_classes = (permissions.IsAuthenticated,)

    @decorators.action(detail=True, methods=["get"])
    def replies(self, req: request.Request, pk: int):
        comment = self.get_object()
        queryset = get_comment_replies(comment=comment)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
