# messaging/routing.py
from django.urls import path
from . import consumers

# Note: The 'app_name' is optional for WebSocket routing but can help with organization.
app_name = 'messaging'

websocket_urlpatterns = [
    # This pattern routes WebSocket connections matching /ws/chat/<recipient_id>/ to our consumer.
    path('ws/chat/<int:recipient_id>/', consumers.ChatConsumer.as_asgi(), name='chat'),
]
