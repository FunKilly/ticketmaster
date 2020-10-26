from datetime import datetime

from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common_utils.mixins import GetSerializerClassMixin

from .models import Event
from .serializers import (
    EventDetailSerializer,
    EventListSerializer,
    EventManagementDetailSerializer,
    EventManagementListSerializer,
    EventReservationsSerializer,
    EventTicketManagementCreateSerializer,
)
from .tasks import add_tickets


class EventManagementViewSet(GetSerializerClassMixin, ModelViewSet):
    serializer_class = EventManagementListSerializer
    queryset = Event.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_action_classes = {
        "create": EventManagementDetailSerializer,
        "list": EventManagementListSerializer,
        "create_tickets": EventTicketManagementCreateSerializer,
        "retrieve": EventManagementDetailSerializer,
        "reservation_stats": EventReservationsSerializer,
        "update": EventManagementDetailSerializer,
        "partial_update": EventManagementDetailSerializer,
    }

    @action(
        methods=["post"],
        detail=True,
        url_path="create-tickets",
        url_name="create_tickets",
    )
    def create_tickets(self, request, pk):
        event = self.get_object()
        if event:
            serializer = self.get_serializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            add_tickets.delay(event_pk=event.id, data=serializer.data)
            return Response("Zlecenie przyjęte do realizacji", status=status.HTTP_200_OK)
        else:
            return Response("Event nie istnieje", status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["get"],
        detail=True,
        url_path="reservation-stats",
        url_name="reservation_stats",
    )
    def reservation_stats(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class EventViewSet(
    GetSerializerClassMixin,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = (permissions.AllowAny,)
    queryset = Event.objects.filter(event_date__gt=datetime.now(), status="active")
    serializer_class = EventListSerializer
    serializer_action_classes = {
        "retrieve": EventDetailSerializer,
        "list": EventListSerializer,
    }
