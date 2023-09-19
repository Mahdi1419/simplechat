# chat/consumers.py
import json
from django.shortcuts import redirect
from channels.db import database_sync_to_async
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from .models import Topic, Message





class ChatConsumer(AsyncWebsocketConsumer):


    # database
    @database_sync_to_async
    def get_messages(self, topic, user):
        messages_objects = Message.objects.filter(topic__uuid=topic).values('id','text', 'sender__username', 'date_time')
        return [
            {
                "id":item.get('id'),
                "text" : item.get('text'),
                "username" : item.get('sender__username'),
                "datetime" : str(item.get('date_time'))
            } 
            for item in messages_objects
        ]

        

    @database_sync_to_async
    def set_message(self, message, topic, user):
        topic_obj = Topic.objects.get(uuid=topic)
        new_message = Message.objects.create(
            topic=topic_obj,
            text=message,
            sender=user
        )

        return {
            "id":new_message.id,
            "text" : new_message.text,
            "username" : new_message.sender.get_username(),
            "datetime" : str(new_message.date_time)
        } 


    async def exec_command(self, command:str, *args, **kwargs):
        commands = {
            "load_message": self.load_message,
            "new_message": self.new_message,
        }
        await commands[command](*args, **kwargs)


    async def load_message(self, *arg, **kwargs):
        pass


    async def new_message(self, *arg, **kwargs):
        pass



    async def connect(self):

        self.user = self.scope['user']
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        command = text_data_json["command"]

        if command == 'load_data':
            messages = await self.get_messages(self.room_name, self.user)
            await self.send(text_data=json.dumps({"message": messages, 'command': command}))

        else:
            print(self.user.username)
            # Send message to room group
            message = await self.set_message(message, self.room_name, self.user)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": self.user.username}))