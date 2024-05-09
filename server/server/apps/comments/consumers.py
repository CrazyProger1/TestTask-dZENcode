import logging
from dataclasses import dataclass, field

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User, AnonymousUser

from .constants import COMMENTS_GROUP
from .enums import WebsocketEvent, WebsocketError

logger = logging.getLogger(__name__)


@dataclass
class Event:
    type: str
    user: User | AnonymousUser
    data: dict = field(default_factory=dict)


class CommentConsumer(AsyncJsonWebsocketConsumer):
    group = COMMENTS_GROUP

    async def _send_response(self, success: bool, data: dict = None):
        logger.info(f"Sending response: {data}")
        await self.send_json({
            "success": success,
            "data": data,
        })

    async def _send_error(self, detail: str):
        await self._send_response(success=False, data={"detail": detail})

    async def _parse_event(self, content: dict) -> Event | None:
        try:
            event = Event(**content, user=self.scope["user"])
            logger.info(f"Received event: {event}")
            return event
        except TypeError:
            logger.info(f"Got message with invalid format: {content}")
            await self._send_error(detail=WebsocketError.INVALID_FORMAT)

    async def _create_comment(self, event: Event):
        if isinstance(event.user, AnonymousUser):
            await self._send_error(detail=WebsocketError.NOT_AUTHENTICATED)

    async def _list_comments(self, event: Event):
        pass

    async def _handle_event(self, event: Event):
        match event.type:
            case WebsocketEvent.CREATE_COMMENT:
                await self._create_comment(event=event)
            case WebsocketEvent.LIST_COMMENTS:
                await self._list_comments(event=event)
            case _:
                await self._send_error(detail=WebsocketError.INVALID_EVENT)

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            group=self.group,
            channel=self.channel_name
        )

        logger.info(f"Client connected: {self.channel_name}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            group=self.group,
            channel=self.channel_name
        )

        logger.info(f"Client disconnected: {self.channel_name}")

    async def receive_json(self, content: dict, **kwargs):
        event = await self._parse_event(content=content)

        if event:
            await self._handle_event(event=event)
