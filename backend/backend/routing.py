from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/ssh/", consumers.ChatConsumer.as_asgi()),
    ])
})
