from django.urls import re_path

from .views import api_v1_docs_view

urlpatterns = [
    re_path(
        r"docs/swagger(?P<format>\.json|\.yaml)",
        api_v1_docs_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"docs/swagger/",
        api_v1_docs_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"docs/redoc/",
        api_v1_docs_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
