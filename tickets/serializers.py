from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Ticket, UserTicket


class TicketDetailSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name')

    class Meta:
        model = Ticket
        fields = ["event_name", "ticket_type", "price", "created_at"]
  

class UserTicketListSerializer(serializers.ModelSerializer):
    ticket = TicketDetailSerializer()

    class Meta:
        model = UserTicket
        fields = ["id", "status", "ticket"]


class UserTicketDetailSerializer(serializers.ModelSerializer):
    ticket = TicketDetailSerializer()

    class Meta:
        model = UserTicket
        fields = ["status", "ticket"]


class UserTicketCreateSerializer(serializers.ModelSerializer):
    ticket_type = serializers.ChoiceField(["regular", "vip", "premium"])
    amount = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        model = UserTicket
        fields = ["ticket_type", "amount"]
