import json

from channels.generic.websocket import AsyncWebsocketConsumer

from project.constants import ChannelGroup


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            self.personal_group = ChannelGroup.PERSONAL.format(user.id)
            self.public_groups = [ChannelGroup.NOTIFICATION]
            self.groups = [*self.public_groups, self.personal_group]
            for group in self.groups:
                await self.channel_layer.group_add(group, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(self.personal_group, {"type": "get.message", "message": message})

    async def get_message(self, event):
        message = event['message']
        await self.send(text_data=message)
