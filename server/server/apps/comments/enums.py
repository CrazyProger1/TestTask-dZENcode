from enum import Enum


class WebsocketEvent(str, Enum):
    CREATE_COMMENT = "comments:create"
    LIST_COMMENTS = "comments:list"


class WebsocketError(str, Enum):
    INVALID_FORMAT = "Invalid format"
    INVALID_EVENT = "Invalid event"
    NOT_AUTHENTICATED = "Not authenticated"
