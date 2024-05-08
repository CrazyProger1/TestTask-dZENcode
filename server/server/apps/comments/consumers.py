import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class CommentConsumer(AsyncJsonWebsocketConsumer):
    @classmethod
    async def decode_json(cls, text_data):
        return {}
        # return json.loads(text_data)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
