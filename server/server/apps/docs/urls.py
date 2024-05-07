from django.urls import re_path

from .views import api_v1_docs_view

urlpatterns = [
    re_path(
        r"api/v1/swagger(?P<format>\.json|\.yaml)",
        api_v1_docs_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"api/v1/swagger/",
        api_v1_docs_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"api/v1/redoc/",
        api_v1_docs_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]