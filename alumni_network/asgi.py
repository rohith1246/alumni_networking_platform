import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_network.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # Add this import
import messaging.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # Wrap URLRouter with AuthMiddlewareStack
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})