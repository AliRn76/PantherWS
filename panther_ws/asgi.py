from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f'[Connect] --> {self.scope=})')
        await self.accept()
        print(f'[Accepted]')
        await self.send(text_data='"Hi"')
        print(f'[Sent Hi]')

    async def receive(self, text_data=None, bytes_data=None):
        print(f'[Received] --> {text_data}')
        if text_data == '"ping"':
            await self.send(text_data='"pong"')

    async def disconnect(self, close_code):
        print(f'[Disconnect] -> {close_code}')
        return self.close()

    async def send_message(self, event):
        message: str = event['text']
        await self.send(text_data=message)


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        re_path(r'^.*$', WSConsumer.as_asgi())
    ]),
})
