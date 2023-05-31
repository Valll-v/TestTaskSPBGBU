from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from organizations.models import Organization
from organizations.serializers import OrgSerializer


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def join_org(request: Request, org_id: int):
    user = request.user
    org = get_object_or_404(Organization, pk=org_id)
    user.organization = org
    user.save()
    return Response()


class OrgViewSet(viewsets.ModelViewSet):
    serializer_class = OrgSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.all()

