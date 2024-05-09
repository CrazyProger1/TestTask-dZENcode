import logging
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User, AnonymousUser

from .exceptions import WebsocketError, AuthError, InvalidEventError

logger = logging.getLogger(__name__)


@dataclass
class Event:
    type: str
    user: User | AnonymousUser
    data: dict = field(default_factory=dict)


class EventBasedAsyncWebsocketConsumer(AsyncJsonWebsocketConsumer):
    group: str
    handlers = {}

    async def connect(self):
        await self.accept()

        await self._handle_event(event=Event(
            type="connected",
            user=self.scope["user"]
        ))

        logger.info(f"Client connected: {self.channel_name}")

    async def disconnect(self, code):
        await self._handle_event(event=Event(
            type="disconnected",
            user=self.scope["user"]
        ))

        logger.info(f"Client disconnected: {self.channel_name}")

    @classmethod
    def event(cls, event_type: str, /, *, auth_required: bool = False):
        def decorator(target: Callable):
            @wraps(target)
            async def wrapper(consumer, event: Event):
                if auth_required:
                    if isinstance(event.user, AnonymousUser):
                        raise AuthError()
                return await target(consumer, event)

            cls.handlers[event_type] = wrapper
            return wrapper

        return decorator

    async def _send_response(self, success: bool, data: dict | None = None):
        logger.info(f"Sending response: {data}")

        await self.send_json(
            {
                "success": success,
                "data": data,
            }
        )

    async def _send_error(self, detail: str):
        await self._send_response(success=False, data={"detail": detail})

    async def _parse_event(self, content: dict) -> Event | None:
        try:
            event = Event(**content, user=self.scope["user"])
            logger.info(f"Received event: {event}")
            return event
        except TypeError:
            logger.info(f"Got message with invalid format: {content}")
            await self._send_error(detail="Invalid format")

    async def _handle_event(self, event: Event):
        handler = self.handlers.get(event.type)
        if callable(handler):
            return await handler(self, event)

        raise InvalidEventError()

    async def receive_json(self, content: dict, **kwargs):
        try:

            event = await self._parse_event(content=content)

            if event:
                response = await self._handle_event(event=event)
                await self._send_response(
                    success=True,
                    data=response
                )

        except WebsocketError as e:
            logger.error(f"Error occurred: {e}")
            await self._send_error(
                detail=e.detail,
            )
