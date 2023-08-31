from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import URLRouter
from django.urls import re_path


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(f'[Connect] --> {self.scope=})')
        await self.accept()
        print(f'[Connected]')

    async def receive(self, text_data=None, bytes_data=None):
        print(f'[Received] --> {text_data}')
        # await self.send(text_data=text_data[::-1])

    async def disconnect(self, close_code):
        print(f'[Disconnect] -> {close_code}')
        return self.close()


application = URLRouter([re_path(r'^.*$', WSConsumer.as_asgi())])
