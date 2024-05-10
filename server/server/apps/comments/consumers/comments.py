from channels.db import database_sync_to_async

from server.apps.comments.constants import COMMENTS_GROUP
from server.apps.comments.enums import WebsocketEvents
from server.apps.comments.serializers import CommentSerializer
from server.apps.comments.exceptions import ValidationError
from server.apps.comments.services import get_parent_comments
from server.utils.django.channels.consumers import (
    EventBasedAsyncWebsocketConsumer,
    Event,
)


class CommentConsumer(EventBasedAsyncWebsocketConsumer):
    group = COMMENTS_GROUP

    async def comment_create(self, event: dict):
        await self.send_json(content=event)


@database_sync_to_async
def create_comment_in_db(serializer: CommentSerializer, user) -> dict:
    serializer.save(user=user)
    return serializer.data


@database_sync_to_async
def read_comments_from_db(
        order_by: tuple[str] = ("id",),
        filters: dict | None = None,
        pagination: tuple = (25, 0),
):
    if not filters:
        filters = {}

    limit, offset = pagination

    comments = get_parent_comments()

    queryset = comments.order_by(*order_by).filter(**filters)[offset: offset + limit]
    serializer = CommentSerializer(data=queryset, many=True)
    serializer.is_valid()

    return {
        "count": comments.count(),
        "results": serializer.data,
    }


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
        },
    )
    return data


@CommentConsumer.event(WebsocketEvents.READ_COMMENTS)
async def read_comments(consumer: CommentConsumer, event: Event):
    order_by = event.data.get("order_by", ("-created_at",))
    filters = event.data.get("filters", {})
    limit = event.data.get("limit", 25)
    offset = event.data.get("offset", 0)

    return await read_comments_from_db(
        order_by=order_by,
        filters=filters,
        pagination=(limit, offset),
    )
