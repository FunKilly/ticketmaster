from datetime import datetime
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event
from .serializers import EventDetailSerializer, EventListSerializer, EventManagementListSerializer, EventTicketSerializer, EventManagementDetailSerializer
from .tasks import add_tickets

from common_utils.mixins import GetSerializerClassMixin


class EventManagementViewSet(GetSerializerClassMixin, ModelViewSet):
    serializer_class = EventManagementListSerializer
    queryset = Event.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_action_classes = {
        "list": EventManagementListSerializer,
        "create_tickets": EventTicketSerializer,
        "retrieve": EventManagementDetailSerializer
    }

    @action(methods=['post'], detail=True, url_path="create-tickets", url_name="create_tickets")
    def create_tickets(self, request, pk):
        event = Event.objects.filter(pk=pk).first()
        if event:
            serializer = self.get_serializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            add_tickets.delay(event_pk=event.id, data=serializer.data)
            return Response("Zlecenie przyjęte do realizacji", status=status.HTTP_200_OK)
        else:
            return Response("Event nie istnieje", status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(GetSerializerClassMixin, GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = (permissions.AllowAny,)
    queryset = Event.objects.filter(event_date__gt=datetime.now())
    serializer_class = EventListSerializer
    serializer_action_classes = {
        "retrieve": EventDetailSerializer,
        "list": EventListSerializer,
        
    }

    
