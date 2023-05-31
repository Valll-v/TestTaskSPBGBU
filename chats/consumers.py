import json

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from loguru import logger

from chats.models import Message, Chat

User = get_user_model()


class WSConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        args = self.scope['path'].split('/')
        token = args[-1]
        try:
            user = await self.get_user(token)
        except TokenError:
            logger.info(f'Invalid Token: {token}')
            return
        self.room_name = user.id
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    @database_sync_to_async
    def get_user(self, token):
        access_token = AccessToken(token)
        return User.objects.filter(id=access_token['user_id']).first()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def new_message(self, from_id, to_id, message):
        chat = Chat.objects.filter(users__in=[from_id]).filter(users__in=[to_id]).first()
        if not chat:
            chat = Chat.objects.create()
            chat.users.add(from_id)
            chat.users.add(to_id)
        Message.objects.create(
            chat=chat,
            text=message,
            owner_id=from_id,
        )
        return chat.id

    async def receive(self, text_data=None, bytes_data=None):
        logger.debug(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        to = text_data_json.get('to')

        chat_id = await self.new_message(from_id=int(self.room_name), to_id=int(to), message=message)

        await self.channel_layer.group_send(
            'chat_' + to,
            {
                'type': 'chat_message',
                'from': self.room_name,
                'message': message,
                'id': chat_id,
            }
        )

        await self.channel_layer.group_send(
            'chat_' + str(self.room_name),
            {
                'type': 'get_chat_id',
                'chat_id': chat_id,
            }
        )

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    async def chat_message(self, event):
        message = event['message']
        user = await self.get_user_by_id(int(event['from']))
        await self.send(text_data=json.dumps({
            'from_name': f'{user.firstname} {user.lastname}',
            'from': event.get('from'),
            'message': message,
            'id': event.get('id'),
            'image': user.photo.url if user.photo else None,
        }, ensure_ascii=False))

    async def get_chat_id(self, event):
        await self.send(text_data=json.dumps({
            'chat_id': event.get('chat_id'),
        }, ensure_ascii=False))
