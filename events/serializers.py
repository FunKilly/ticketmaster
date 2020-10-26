from django.core.validators import MinValueValidator
from django.db.models import Count, Sum
from rest_framework import serializers

from tickets.models import Ticket

from .models import Event


class EventManagementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "event_date",
            "place",
            "status",
            "description",
            "created_at",
            "available_seats",
        ]
        extra_kwargs = {"id": {"read_only": True}, "created_at": {"read_only": True}}


class EventReservationsSerializer(serializers.ModelSerializer):
    quantity_reserved = serializers.SerializerMethodField()
    quantity_reserved_by_ticket_type = serializers.SerializerMethodField()
    tickets_income = serializers.SerializerMethodField()
    finalized_reservations = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "id",
            "quantity_reserved",
            "quantity_reserved_by_ticket_type",
            "tickets_income",
            "finalized_reservations",
        ]
        model = Event

    def get_quantity_reserved(self, obj):
        return obj.tickets.filter(order__status="waiting").count()

    def get_quantity_reserved_by_ticket_type(self, obj):
        return (
            obj.tickets.values("ticket_type")
            .filter(order__status="waiting")
            .annotate(reserved_seats=Count("ticket_type"))
        )

    def get_finalized_reservations(self, obj):
        return obj.tickets.filter(order__status="paid").aggregate(finalized=Count("id"))[
            "finalized"
        ]

    def get_tickets_income(self, obj):
        return obj.tickets.filter(order__status="paid").aggregate(income=Sum("price"))


class EventManagementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "place", "status"]


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "event_date",
            "place",
            "status",
            "description",
            "available_seats",
        ]


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "place", "status"]


class EventTicketManagementCreateSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        model = Ticket
        fields = ["ticket_type", "price", "amount"]
