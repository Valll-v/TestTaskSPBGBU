from rest_framework import viewsets, permissions


from rest_framework.response import Response
from chats.serializers import *
from django.db.models import OuterRef, Subquery


class ChatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortChatSerializer
        return FullChatSerializer

    def get_queryset(self):
        messages = Message.objects.filter(chat=OuterRef('pk')).order_by('-time')
        chats = self.request.user.chats.annotate(last_msg_time=Subquery(messages.values('time')[:1])
                                                 ).order_by('-last_msg_time').all()
        return chats

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.get_serializer_class()
        return Response(self.serializer_class(self.get_queryset(), many=True, context={'request': request}).data)
