from rest_framework import serializers
from rest_framework.decorators import api_view

from events.models import Event
from organizations.serializers import OrgSerializer
from users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    organizers = OrgSerializer(source='organizations', read_only=True, many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'organizers', 'image', 'date', 'organizations')
