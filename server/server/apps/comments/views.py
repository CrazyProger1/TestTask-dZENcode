from rest_framework import viewsets

from .services import get_all_comments
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = get_all_comments()
    serializer_class = CommentSerializer
    page_size = 35
