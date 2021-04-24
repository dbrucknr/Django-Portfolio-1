from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
import json
from channels.db import database_sync_to_async

class MessageConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def _get_user_group(self, user):
        return user.groups.first().name

    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            user_group = await self._get_user_group(user)
            await self.channel_layer.group_add(
                group=user_group,
                channel=self.channel_name
            )    
            await self.accept()

    async def disconnect(self, code):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            user_group = await self._get_user_group(user)
            await self.channel_layer.group_discard(
                group=user_group,
                channel=self.channel_name
            )
        await super().disconnect(code)

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'echo.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })
    # async def send_channel_message(self, group_name, message):
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         '{}'.format(group_name),
    #         {
    #             'type': 'channel_message',
    #             'message': message
    #         }
    #     )

    # # Receive message from the group
    # async def receive_channel_message(self, event):
    #     message = event['message']
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))