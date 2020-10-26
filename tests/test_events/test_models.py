from datetime import datetime, timedelta

from django.test import TestCase

from events.models import Event
from tickets.models import Ticket


class TestEventModel(TestCase):
    def setUp(self):
        future_data = datetime.now() + timedelta(days=10)
        self.event = Event.objects.create(
            name="The Real Slim Shady", event_date=future_data, place="Mars"
        )

    def test_create_tickets(self):
        data = {"price": 130, "amount": 1000, "ticket_type": "regular"}
        self.event.create_tickets(data)

        tickets_count = Ticket.objects.filter(
            event=self.event, ticket_type=data["ticket_type"], price=data["price"]
        ).count()

        self.assertEqual(tickets_count, data["amount"])

    def test_available_seats(self):
        data = {"price": 130, "amount": 1000, "ticket_type": "regular"}
        self.event.create_tickets(data)

        self.assertEqual(
            self.event.available_seats[0]["ticket_type"], data["ticket_type"]
        )
        self.assertEqual(self.event.available_seats[0]["available_seats"], data["amount"])
