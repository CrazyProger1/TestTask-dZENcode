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
        pass

    raise ValidationError()


@CommentConsumer.event(WebsocketEvents.LIST_COMMENTS)
async def list_comments(consumer: CommentConsumer, event: Event):
    pass
