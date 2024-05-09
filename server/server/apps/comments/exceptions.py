from server.utils.django.channels.consumers.exceptions import WebsocketError


class ValidationError(WebsocketError):
    type = "ValidationError"
