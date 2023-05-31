from rest_framework import viewsets, permissions
from django.core.paginator import Paginator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
from events.models import Event
from events.serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Event.objects.all()

    def list(self, request: Request, *args, **kwargs):
        events = Paginator(self.filter_queryset(self.get_queryset()), 3)
        return Response(self.serializer_class(events.get_page(request.GET.get('page')),
                                              many=True, context={'request': request}).data)


