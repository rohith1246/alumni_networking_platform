import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject connection if user is not authenticated
            await self.close()
            return

        try:
            # Get the recipient's ID from the URL parameters
            self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
            self.sender_id = self.scope['user'].id

            # Validate that recipient exists
            recipient_exists = await self.check_recipient_exists(self.recipient_id)
            if not recipient_exists:
                await self.close()
                return

            # Create a unique room name based on both user IDs (sorted for consistency)
            ids = sorted([str(self.sender_id), str(self.recipient_id)])
            self.room_group_name = f'chat_{ids[0]}_{ids[1]}'

            # Join the room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            print(f"Connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'room_group_name'):
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
        except Exception as e:
            print(f"Disconnect error: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()
            if not message:
                return

            # Save the message to the database
            saved_message = await self.save_message(
                self.scope['user'].id, 
                self.recipient_id, 
                message
            )

            if saved_message:
                # Retrieve the sender's profile picture URL
                sender_profile_pic_url = await self.get_sender_profile_pic_url(self.scope['user'].id)

                # Broadcast the message to everyone in the room
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_id': self.scope['user'].id,
                        'sender_username': self.scope['user'].username,
                        'sender_profile_pic_url': sender_profile_pic_url,
                        'timestamp': saved_message.timestamp.isoformat(),
                    }
                )
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Receive error: {str(e)}")

    async def chat_message(self, event):
        try:
            # Send the message data (including the sender's profile pic URL) to the WebSocket client
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender_id': event['sender_id'],
                'sender_username': event['sender_username'],
                'sender_profile_pic_url': event.get('sender_profile_pic_url'),
                'timestamp': event.get('timestamp'),
            }))
        except Exception as e:
            print(f"Chat message error: {str(e)}")

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, message):
        try:
            sender = User.objects.get(id=sender_id)
            recipient = User.objects.get(id=recipient_id)
            return Message.objects.create(
                sender=sender, 
                recipient=recipient, 
                body=message
            )
        except User.DoesNotExist:
            return None
        except Exception as e:
            print(f"Save message error: {str(e)}")
            return None

    @database_sync_to_async
    def check_recipient_exists(self, recipient_id):
        return User.objects.filter(id=recipient_id).exists()

    @database_sync_to_async
    def get_sender_profile_pic_url(self, sender_id):
        try:
            sender = User.objects.get(id=sender_id)
            if sender.profile_pic:
                return sender.profile_pic.url
            else:
                return "/static/default.jpg"
        except Exception as e:
            print(f"Error fetching profile pic: {str(e)}")
            return "/static/default.jpg"
