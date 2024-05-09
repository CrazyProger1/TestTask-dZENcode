from dataclasses import dataclass


class WebsocketError(Exception):
    detail: str

    def __init__(self):
        super().__init__(self.detail)


class AuthError(WebsocketError):
    detail = "Authentication required"


class InvalidEventError(WebsocketError):
    detail = "Invalid event"
