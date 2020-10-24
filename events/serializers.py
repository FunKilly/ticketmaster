from django.core.validators import MinValueValidator

from rest_framework import serializers

from .models import Event

from tickets.models import Ticket


class EventManagementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "place", "status", "description", "created_at", "available_seats"]
        extra_kwargs = {"id": {"read_only": True}, "created_at": {"read_only": True}}


class EventManagementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "place", "status"]



class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "place", "status", "description", "available_seats"]


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "place", "status"]


class EventTicketSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        model = Ticket
        fields = ["ticket_type", "price", "amount"]
        