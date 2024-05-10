import logging

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.db import close_old_connections

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from jwt import decode

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseMiddleware):
    @database_sync_to_async
    def _get_user(self, pk: int):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return AnonymousUser()

    @staticmethod
    def _decode_jwt(token: bytes) -> dict:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.SIMPLE_JWT["ALGORITHM"],
        )
        return payload

    def _get_token(self, scope) -> bytes | None:
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            return headers[b"authorization"].split()[1]

    async def _authenticate(self, scope):
        try:
            token = self._get_token(scope=scope)
            if token:
                payload = self._decode_jwt(token=token)
                user = await self._get_user(pk=payload["user_id"])
                scope["user"] = user
                logger.info(f"User authenticated: {user}")
                return
        except Exception as e:
            logger.warning(f"User not authenticated: {type(e).__name__}: {e}")

        scope["user"] = AnonymousUser()

    async def __call__(self, scope, receive, send):
        logger.info(f"Trying to authenticate user using {type(self).__name__}...")
        close_old_connections()
        await self._authenticate(scope=scope)
        return await super().__call__(scope, receive, send)
