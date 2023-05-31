from rest_framework import serializers
from django.db.models import Q
from users.models import CustomUser
from chats.models import Chat, Message
from users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'time', 'text', 'sender', 'unread')


class FullChatSerializer(serializers.ModelSerializer):
    messages_list = MessageSerializer(many=True, source='messages', read_only=True)
    chat_with = serializers.SerializerMethodField()

    def get_chat_with(self, obj: Chat):
        user: CustomUser = self.context['request'].user
        user_with = obj.users.filter(~Q(id=user.id)).first()
        obj.messages.filter(owner=user_with, unread=True).update(unread=False)
        return UserSerializer(user_with).data

    class Meta:
        model = Chat
        fields = ('chat_with', 'messages_list')


class ShortChatSerializer(serializers.ModelSerializer):
    last_msg = serializers.SerializerMethodField()
    chat_with = serializers.SerializerMethodField()
    count_unread_messages = serializers.SerializerMethodField()

    def get_chat_with(self, obj: Chat):
        user: CustomUser = self.context['request'].user
        user_with = obj.users.filter(~Q(id=user.id)).first()
        return UserSerializer(user_with).data

    def get_count_unread_messages(self, obj: Chat):
        user: CustomUser = self.context['request'].user
        user_with = obj.users.filter(~Q(id=user.id)).first()
        return obj.messages.filter(owner=user_with, unread=True).count()

    def get_last_msg(self, obj: Chat):
        message = obj.messages.last()
        if message:
            return MessageSerializer(message).data

    class Meta:
        model = Chat
        fields = ('id', 'chat_with', 'last_msg', 'count_unread_messages')

