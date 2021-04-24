from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from server.middleware import TokenAuthMiddlewareStack
from messenger.consumers import MessageConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path('messenger/', MessageConsumer.as_asgi()),
        ]),
    ),
})