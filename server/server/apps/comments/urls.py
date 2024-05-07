from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet

router = routers.DefaultRouter()
router.register("comments", CommentViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls))
]
