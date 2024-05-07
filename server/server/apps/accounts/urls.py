from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        "api/v1/users/login/", TokenObtainPairView.as_view(), name="tokens-obtain-pair"
    ),
    path("api/v1/users/refresh/", TokenRefreshView.as_view(), name="tokens-refresh"),
    path("api/v1/", include("djoser.urls")),
]