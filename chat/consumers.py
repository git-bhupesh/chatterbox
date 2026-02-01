import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
    # Grabbing 'room_id' because that's what we named it in routing.py
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        # ... rest of your code ...

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('message')
        user = self.scope['user']

        if user.is_authenticated and content:
            # We use the room_id we captured in connect()
            await self.save_message(self.room_id, user, content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': content,
                    'sender': user.username,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    # --- ADD/UPDATE THIS METHOD AT THE BOTTOM ---
    @database_sync_to_async
    def save_message(self, room_id, user, content):
        try:
            # Finding the actual Room object in the DB
            room = ChatRoom.objects.get(id=room_id)
            return Message.objects.create(room=room, sender=user, content=content)
        except ChatRoom.DoesNotExist:
            return None