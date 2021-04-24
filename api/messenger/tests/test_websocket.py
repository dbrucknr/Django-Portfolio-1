import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from server.routing import application
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import Group
from messenger.models import Message

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@database_sync_to_async
def create_user(
        username, 
        email, 
        password
    ):
    
    user = get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.save()
    user_group, _ = Group.objects.get_or_create(name="user-{}".format(user.id))
    user.groups.add(user_group)

    access = AccessToken.for_user(user)
    return user, access

@database_sync_to_async
def create_message(
    content="Creating test message",
    sender=None,
    receiver=None
):
    return Message.objects.create(
        content=content,
        sender=sender,
        receiver=receiver
    ) 
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:

    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'testUser', 'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/messenger/?token={access}'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'testUser', 'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/messenger/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/messenger/'
        )
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    async def test_join_own_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            username='testUser', email='test.user@example.com', password='pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/messenger/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send("user-{}".format(user.id), message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_send_message(self, settings):
        """ Tests the creation of message to a sender """

        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            'testUser', 'test.user@example.com', 'pAssw0rd'
        )
        receiver, access = await create_user(
            'receiverUser', 'receiver.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/messenger/?token={access}'
        )
        connected, _ = await communicator.connect()
        await communicator.send_json_to({
            'type': 'create.message',
            'data': {
                'content': 'This is a message',
                'sender': user.id,
                'receiver': receiver.id
            },
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')
        assert response_data['id'] is not None
        assert response_data['content'] == 'This is a message'
        assert response_data['sender']['username'] == user.username
        assert response_data['receiver']['username'] == receiver.username
        await communicator.disconnect()

    async def test_receiver_alerted_on_sent_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        sender, access = await create_user(
            'testUser', 'test.user@example.com', 'pAssw0rd'
        )
        receiver, _ = await create_user(
            'receiverUser', 'receiver.user@example.com', 'pAssw0rd'
        )
        # Listen to the user's group test channel.
        channel_layer = get_channel_layer()
        await channel_layer.group_add(
            group="user-{}".format(receiver.id),
            channel='test_channel'
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/messenger/?token={access}'
        )
        connected, _ = await communicator.connect()
        # Send a message.
        await communicator.send_json_to({
            'type': 'create.message',
            'data': {
                'content': 'This is a message',
                'sender': sender.id,
                'receiver': receiver.id
            },
        })

        # Receive JSON message from server on test_channel.
        response = await channel_layer.receive('test_channel')
        response_data = response.get('data')

        assert response_data['id'] is not None
        assert response_data['content'] == 'This is a message'
        assert response_data['sender']['username'] == sender.username
        assert response_data['receiver']['username'] == receiver.username

        await communicator.disconnect()

    async def test_create_message_group(self, settings):

        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            'testUser', 'test.user@example.com', 'pAssw0rd'
        )
        receiver, _ = await create_user(
            'receiverUser', 'receiver.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/messenger/?token={access}'
        )
        connected, _ = await communicator.connect()

        # Send a message.
        await communicator.send_json_to({
            'type': 'create.message',
            'data': {
                'content': 'This is a message',
                'sender': user.id,
                'receiver': receiver.id
            },
        })

        response = await communicator.receive_json_from()
        response_data = response.get('data')

        # Send a message to the reciever's group.
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        formatted_user_group = "user-{}".format(response_data['receiver']['id'])

        channel_layer = get_channel_layer()
        await channel_layer.group_send(formatted_user_group, message=message)

        # Receiver receives message.
        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()

