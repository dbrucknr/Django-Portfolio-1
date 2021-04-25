from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
import json
from channels.db import database_sync_to_async
from messenger.api.serializers import NestedMessageSerializer, MessageSerializer
class MessageConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = 'app'
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        text_data = json.loads(text_data)
        sender = text_data['data']['sender']
        message = text_data['data']['content']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'create.message',
                'sender': sender,
                'message': message
            }
        )

    # Receive message from room group
    async def create_message(self, event):
        message = event['message']
        sender = event['sender']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message
        }))