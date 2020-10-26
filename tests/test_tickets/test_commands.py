from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from events.models import Event
from tickets.models import Order, Ticket

UserModel = get_user_model()


class TestUpdateStatusesCommand(TestCase):
    def test_command(self):
        future_date = datetime.now() + timedelta(days=+14)
        event = Event.objects.create(
            name="Jakub Wedrowycz in Belweder", place="Warszawa", event_date=future_date
        )

        data = {"price": 120, "amount": 1000, "ticket_type": "regular"}
        event.create_tickets(data)

        owner = UserModel.objects.create(
            name="Stephen King", email="dark_tower@gmail.com", password="Test1234!"
        )
        order = Order.objects.create(event=event, owner=owner)

        tickets = Ticket.objects.filter(event=event)[:10]
        tickets_ids = [ticket.id for ticket in tickets]

        order.attach_tickets(tickets_ids)

        past_date = datetime.now() + timedelta(minutes=20)
        order.created_at = past_date
        order.save()

        tickets_count = Ticket.objects.filter(id__in=tickets_ids, status="booked").count()

        self.assertEqual(len(tickets_ids), tickets_count)

        call_command("update_statuses_command",)

        tickets_count = Ticket.objects.filter(id__in=tickets_ids, status="booked").count()

        self.assertEqual(tickets_count, 0)
