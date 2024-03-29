import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from decouple import config
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE"))

# Setup Django before loading the application.
django.setup()


# Import the WebSocket routing definitions from each app after Django has been set up.
from assistant.routing import websocket_urlpatterns as assistant_websocket_urlpatterns
from notifications.routing import (
    websocket_urlpatterns as notifications_websocket_urlpatterns,
)

# Combine all the WebSocket URL patterns.
websocket_urlpatterns = (
    assistant_websocket_urlpatterns + notifications_websocket_urlpatterns
)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
