from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
import json
from channels.db import database_sync_to_async
from messenger.api.serializers import NestedMessageSerializer, MessageSerializer
class MessageConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def _get_user_group(self, user):
        return user.groups.first().name

    @database_sync_to_async
    def _create_message(self, data):
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)


    @database_sync_to_async
    def _get_message_data(self, message):
        return NestedMessageSerializer(message).data

    @database_sync_to_async
    def _get_message_sender_ids(self, user):
        user_groups = user.groups.values_list('name', flat=True)
        print(user_groups)
        # if 'driver' in user_groups:
        #     trip_ids = user.trips_as_driver.exclude(
        #         status=Trip.COMPLETED
        #     ).only('id').values_list('id', flat=True)
        # else:
        #     trip_ids = user.trips_as_rider.exclude(
        #         status=Trip.COMPLETED
        #     ).only('id').values_list('id', flat=True)
        # return map(str, trip_ids)

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

    async def create_message(self, message):
        data = message.get('data')
        created_message = await self._create_message(data)
        created_message_data = await self._get_message_data(created_message)

        # Sends message to receivers group
        await self.channel_layer.group_send(group="user-{}".format(data['receiver']), message = {
            'type': 'echo.message',
            'data': created_message_data
        })

        # Add sender to receivers group.
        # I think this is messed up
        receiver_id = data['receiver']
        await self.channel_layer.group_add( # new
            group=f'user-{receiver_id}',
            channel=self.channel_name
        )

        await self.send_json({
          'type': 'echo.message',
          'data': created_message_data,
        })

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
        await self.send_json(message)

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'create.message':
            await self.create_message(content)
        if message_type == 'echo.message':
            await self.echo_message(content)

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