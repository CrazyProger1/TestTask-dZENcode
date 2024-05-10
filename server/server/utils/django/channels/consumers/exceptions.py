class WebsocketError(Exception):
    type: str = "WebsocketError"
    details: str | None = None

    def __init__(self, details: str | None = None):
        self.details = details
        super().__init__(self.type)


class AuthenticationError(WebsocketError):
    type = "AuthenticationError"


class InvalidEventError(WebsocketError):
    type = "InvalidEventError"


class InvalidFormatError(WebsocketError):
    type = "InvalidFormatError"
