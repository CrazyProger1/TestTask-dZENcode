from django.urls import path, include
from rest_framework import routers

from .views import (
    CommentViewSet,
    CommentLikeViewSet,
    ReplyViewSet,
    CommentAttachmentViewSet
)

router = routers.DefaultRouter()

router.register(
    r"comments",
    CommentViewSet,
    basename="comments",
)
router.register(
    r"comments/(?P<comment_id>\d+)/likes",
    CommentLikeViewSet,
    basename="comment-likes",
)
router.register(
    r"comments/(?P<comment_id>\d+)/replies",
    ReplyViewSet,
    basename="comment-replies",
)
router.register(
    r"comments/(?P<comment_id>\d+)/attachments",
    CommentAttachmentViewSet,
    basename="comment-attachments",
)
urlpatterns = [
    path("api/v1/", include(router.urls)),
]
