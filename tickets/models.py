import uuid
from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from events.models import Event

from .constants import TicketStatusType, TicketType


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=15, choices=TicketType.choices, default=TicketType.REGULAR,)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.0)])
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserTicket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    number_of_seats = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    price = models.DecimalField(max_digits=22, decimal_places=2, validators=[MinValueValidator(0.0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=TicketStatusType.choices, default=TicketStatusType.BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def active(self):
        if self.status == TicketStatusType.PAID:
            return True
        elif self.status == TicketStatusType.CANCELED:
            return False
        else:
            diff = datetime.now() - self.created_at
            return all(diff.seconds < 900, diff.days == 0)


class PaymentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(UserTicket, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)
