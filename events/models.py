import uuid

from django.db import models
from django.db.models import Count

from tickets.models import Ticket
from .constants import EventStatusType

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, blank=False, null=False)
    event_date = models.DateTimeField(blank=False, null=False)
    place = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=EventStatusType.choices, default=EventStatusType.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['name', 'event_date']]

    def create_tickets(self, data):
        tickets = [Ticket(event=self, ticket_type=data["ticket_type"], price=data["price"]) for n in range(data["amount"])]
        Ticket.objects.bulk_create(tickets)

    @property
    def available_seats(self):
        return self.tickets.values("ticket_type").filter(order__isnull=True).annotate(available_seats=Count("ticket_type"))
