from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_v1_docs_view = get_schema_view(
    openapi.Info(
        title=f"{settings.APP} API",
        default_version="v1",
        description=settings.DESCRIPTION,
        contact=openapi.Contact(email=settings.CONTACT_EMAIL),
        license=openapi.License(name=settings.LICENCE),
    ),
    public=True,
)
