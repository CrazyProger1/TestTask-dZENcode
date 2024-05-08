from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet, CommentLikeViewSet

router = routers.DefaultRouter()

router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'comments/(?P<comment_id>\d+)/likes', CommentLikeViewSet, basename='comment-likes')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
