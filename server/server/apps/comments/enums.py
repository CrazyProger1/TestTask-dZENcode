from enum import Enum


class WebsocketEvents(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CREATE_COMMENT = "comments.create"
    READ_COMMENTS = "comments.read"
    READ_REPLIES = "comments.replies.read"
