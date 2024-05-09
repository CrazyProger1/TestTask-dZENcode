from enum import Enum


class WebsocketEvents(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CREATE_COMMENT = "comment.create"
    LIST_COMMENTS = "comment.list"
