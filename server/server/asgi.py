"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from server.apps.comments.urls import ws_urlpatterns
from server.utils.django.channels.jwt import JWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.development")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(URLRouter(ws_urlpatterns)),
    }
)
