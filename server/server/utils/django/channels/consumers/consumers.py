import json
import logging
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User, AnonymousUser

from .exceptions import (
    WebsocketError,
    AuthenticationError,
    InvalidEventError,
    InvalidFormatError,
)

logger = logging.getLogger(__name__)


@dataclass
class Event:
    type: str
    user: User | AnonymousUser
    data: dict = field(default_factory=dict)


class EventBasedAsyncWebsocketConsumer(AsyncJsonWebsocketConsumer):
    group: str
    handlers: dict[str, Callable] = {}

    async def _send_response(
        self, success: bool, data: dict | None = None, event_type: str | None = None
    ):
        logger.info(f"Sending response: {data}")

        await self.send_json(
            {
                "type": event_type,
                "success": success,
                "data": data,
            }
        )

    async def _send_error(self, error: WebsocketError):
        await self._send_response(
            success=False,
            data={
                "error": error.type,
                "details": error.details,
            },
            event_type="error",
        )

    async def _parse_event(self, content: dict) -> Event | None:
        try:
            event = Event(**content, user=self.scope["user"])
            logger.info(f"Received event: {event}")
            return event
        except TypeError:
            raise InvalidFormatError(f"Can't parse event: {content}")

    async def _handle_event(self, event: Event):
        logger.info(f"Handling event: {event}")

        handler = self.handlers.get(event.type)
        if callable(handler):
            return await handler(self, event)

        raise InvalidEventError(f"Event handler not found: {event.type}")

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        try:
            await super().receive(text_data, bytes_data, **kwargs)
        except json.JSONDecodeError as e:
            await self._send_error(InvalidFormatError(str(e)))

    async def connect(self):
        await self.accept()

        await self._handle_event(event=Event(type="connected", user=self.scope["user"]))

        logger.info(f"Client connected: {self.channel_name}")

    async def disconnect(self, code):
        await self._handle_event(
            event=Event(type="disconnected", user=self.scope["user"])
        )

        logger.info(f"Client disconnected: {self.channel_name}")

    @classmethod
    def event(cls, event_type: str, /, *, auth_required: bool = False):
        def decorator(target: Callable):
            @wraps(target)
            async def wrapper(consumer, event: Event):
                if auth_required:
                    if isinstance(event.user, AnonymousUser):
                        raise AuthenticationError("Authorization required")
                return await target(consumer, event)

            cls.handlers[event_type] = wrapper
            return wrapper

        return decorator

    async def receive_json(self, content: dict, **kwargs):
        logger.info(f"Received JSON: {content}")

        try:
            event = await self._parse_event(content=content)

            if event:
                response = await self._handle_event(event=event)
                await self._send_response(
                    success=True, data=response, event_type=event.type
                )

        except WebsocketError as e:
            logger.error(f"{type(e).__name__}: {e}")
            await self._send_error(error=e)
