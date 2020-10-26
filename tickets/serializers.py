from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from .models import Order


class OrderPaymentSerializer(serializers.Serializer):
    # The amount should be send by frontend.
    amount = serializers.DecimalField(decimal_places=2, max_digits=12)
    currency = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ["amount", "currency", "token"]


class OrderCreateSerializer(serializers.Serializer):
    amount = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    event_id = serializers.UUIDField()
    ticket_type = serializers.ChoiceField(choices=["regular", "premium", "vip"])

    class Meta:
        fields = ["amount", "ticket_type", "event_id"]


class OrderDetailSerializer(serializers.ModelSerializer):
    # Frontend shouldn't display status, on its basis, it should check whether the order is paid for
    event_id = serializers.CharField(source="event.id")
    event_name = serializers.CharField(source="event.name")
    event_date = serializers.CharField(source="event.event_date")

    class Meta:
        model = Order
        fields = [
            "id",
            "event_id",
            "event_name",
            "event_date",
            "total_price",
            "created_at",
            "is_active",
            "status",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.name")
    event_date = serializers.CharField(source="event.event_date")

    class Meta:
        model = Order
        fields = ["id", "event_name", "event_date", "is_active"]
