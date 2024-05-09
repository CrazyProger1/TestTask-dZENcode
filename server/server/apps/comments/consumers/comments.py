from channels.db import database_sync_to_async

from server.apps.comments.constants import COMMENTS_GROUP
from server.apps.comments.enums import WebsocketEvents
from server.utils.django.channels.consumers import (
    EventBasedAsyncWebsocketConsumer,
    Event,
)
from server.apps.comments.serializers import CommentSerializer
from server.apps.comments.exceptions import ValidationError


class CommentConsumer(EventBasedAsyncWebsocketConsumer):
    group = COMMENTS_GROUP

    async def comment_create(self, event: dict):
        await self.send_json(content=event)


@database_sync_to_async
def create_comment_in_db(serializer: CommentSerializer, user) -> dict:
    serializer.save(user=user)
    return serializer.data


@CommentConsumer.event(WebsocketEvents.CONNECTED)
async def connected(consumer: CommentConsumer, event: Event):
    await consumer.channel_layer.group_add(
        group=consumer.group, channel=consumer.channel_name
    )


@CommentConsumer.event(WebsocketEvents.DISCONNECTED)
async def disconnected(consumer: CommentConsumer, event: Event):
    await consumer.channel_layer.group_discard(
        group=consumer.group, channel=consumer.channel_name
    )


@CommentConsumer.event(WebsocketEvents.CREATE_COMMENT, auth_required=True)
async def create_comment(consumer: CommentConsumer, event: Event):
    serializer = CommentSerializer(data=event.data)

    if not serializer.is_valid():
        raise ValidationError("Comment data is invalid")

    data = await create_comment_in_db(serializer, event.user)

    await consumer.channel_layer.group_send(
        consumer.group,
        {
            "type": event.type,
            "data": data,
        }
    )
    return data


@CommentConsumer.event(WebsocketEvents.LIST_COMMENTS)
async def list_comments(consumer: CommentConsumer, event: Event):
    pass
