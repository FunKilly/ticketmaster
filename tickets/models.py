import uuid
from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models

from .constants import OrderStatusType, TicketStatusType, TicketType
from .integrations.payment.payment import PaymentGateway, PaymentResult


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="tickets"
    )
    ticket_type = models.CharField(
        max_length=15, choices=TicketType.choices, default=TicketType.REGULAR,
    )
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    status = models.CharField(
        max_length=10, choices=TicketStatusType.choices, default=TicketStatusType.SPARE
    )
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("events.Event", on_delete=models.PROTECT)
    owner = models.ForeignKey("users.User", on_delete=models.PROTECT)
    status = models.CharField(
        max_length=10, choices=OrderStatusType.choices, default=OrderStatusType.WAITING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        tickets = self.ticket_set.aggregate(total_price=models.Sum("price"))
        return tickets["total_price"]

    @property
    def is_active(self):
        if self.status == OrderStatusType.PAID and self.event.event_date > datetime.now():
            return True
        else:
            diff = datetime.now() - self.created_at
            return all([diff.seconds < 900, diff.days == 0])

    def update_tickets_status(self, tickets_ids):
        Ticket.objects.filter(id__in=tickets_ids).update(status="booked")

    def attach_tickets(self, tickets_ids):
        self.update_tickets_status(tickets_ids)
        tickets = Ticket.objects.filter(id__in=tickets_ids)
        self.ticket_set.set(tickets)

    def execute_payment(self, data):
        gateway = PaymentGateway()
        result = gateway.charge(
            amount=data["amount"], token=data["token"], currency=data["currency"]
        )

        if type(result) == PaymentResult:
            self.update_statuses_after_success_payment()
        return result

    def update_statuses_after_success_payment(self):
        self.status = OrderStatusType.PAID
        self.ticket_set.update(status=TicketStatusType.PAID)
        self.save()
