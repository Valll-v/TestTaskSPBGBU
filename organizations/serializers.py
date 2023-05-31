from rest_framework import serializers
from rest_framework.decorators import api_view

from organizations.models import Organization
from users.serializers import UserSerializer


class OrgSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    owner_info = UserSerializer(source='owner', read_only=True)
    users = UserSerializer(many=True, read_only=True)
    full_address = serializers.SerializerMethodField()

    def get_full_address(self, obj: Organization):
        return obj.address + ' ' + obj.postcode

    class Meta:
        model = Organization
        fields = ('id', 'owner', 'owner_info', 'title', 'full_address', 'postcode', 'users')
