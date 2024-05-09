from enum import Enum


class WebsocketEvents(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CREATE_COMMENT = "comments:create"
    LIST_COMMENTS = "comments:list"
