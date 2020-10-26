from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common_utils.mixins import GetSerializerClassMixin
from events.models import Event

from .models import Order, Ticket
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderPaymentSerializer,
)


class OrderViewSet(
    GetSerializerClassMixin,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    CreateAPIView,
):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderListSerializer
    serializer_action_classes = {
        "list": OrderListSerializer,
        "retrieve": OrderDetailSerializer,
        "create": OrderCreateSerializer,
        "make_payment": OrderPaymentSerializer,
    }

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)

    def create(
        self, request, *args, **kwargs,
    ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = Event.objects.filter(id=serializer.validated_data["event_id"]).first()
        if event:
            spare_tickets_ids = self.get_spare_tickets_ids(serializer.validated_data)

            if len(spare_tickets_ids) == serializer.validated_data["amount"]:
                order = Order.objects.create(event=event, owner=request.user)
                order.attach_tickets(spare_tickets_ids)
                return Response(
                    "Tickets has been reserved. After 15 minutes reservation will be released.",
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    "The pool of available tickets is not enough.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response("Event not found.", status=status.HTTP_400_BAD_REQUEST,)

    def get_spare_tickets_ids(self, data):
        tickets_ids = (
            Ticket.objects.filter(event__id=data["event_id"])
            .filter(order__isnull=True)
            .filter(ticket_type=data["ticket_type"])
            .values("id")[: data["amount"]]
        )
        return [ticket["id"] for ticket in tickets_ids]

    @action(
        methods=["post"], detail=True, url_path="make-payment", url_name="make_payment"
    )
    def make_payment(self, request, pk):
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        order = self.get_object()
        if order.is_active == True and order.status == "waiting":
            result = order.execute_payment(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK,)
        elif order.is_active == False:
            return Response("Reservation expired.", status=status.HTTP_400_BAD_REQUEST,)
        else:
            return Response("Order is already paid", status=status.HTTP_400_BAD_REQUEST,)
