from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from events.models import Event
from tickets.integrations.payment.payment import PaymentResult
from tickets.models import Order, Ticket

UserModel = get_user_model()


class TestOrderModel(TestCase):
    def setUp(self):
        future_date = datetime.now() + timedelta(days=10)
        self.event = Event.objects.create(
            name="Powerwolf in Wroclaw",
            event_date=future_date,
            place="Wroclaw",
            description="lorem ipsum",
        )
        self.data = {"price": 130, "amount": 1000, "ticket_type": "regular"}
        self.event.create_tickets(self.data)

        self.owner = UserModel.objects.create_user(
            name="test test", password="Test1234!", email="test@gmail.com"
        )
        self.order = Order.objects.create(event=self.event, owner=self.owner)

        tickets = Ticket.objects.filter(event=self.event)[:5]
        self.tickets_ids = [ticket.id for ticket in tickets]

    def test_total_price(self):
        self.order.attach_tickets(self.tickets_ids)

        total_price = self.data["price"] * 5

        self.assertEqual(self.order.total_price, total_price)

    def test_is_active(self):
        self.assertTrue(self.order.is_active)

        self.order.created_at = datetime.now() + timedelta(minutes=-20)

        self.assertFalse(self.order.is_active)

        self.order.status = "paid"

        self.assertTrue(self.order.is_active)

    def test_update_tickets_status(self):
        self.order.update_tickets_status(self.tickets_ids)

        ticket_count = Ticket.objects.filter(
            id__in=self.tickets_ids, status="booked"
        ).count()

        self.assertEqual(ticket_count, 5)

    def test_attach_tickets(self):
        self.order.attach_tickets(self.tickets_ids)

        tickets = Ticket.objects.filter(id__in=self.tickets_ids)
        order_tickets = self.order.ticket_set.all()

        self.assertEqual(list(tickets), list(order_tickets))

    @patch(
        "tickets.models.PaymentGateway.charge", return_value=PaymentResult("100", "EUR")
    )
    def test_execute_payment(self, mock):
        data = {"amount": 100, "currency": "EUR", "token": "loremipsum"}
        result = self.order.execute_payment(data)

        self.assertEqual(result, mock.return_value)

    def test_update_statuses_after_success_payment(self):
        self.order.attach_tickets(self.tickets_ids)
        self.order.update_statuses_after_success_payment()

        tickets_count = Ticket.objects.filter(
            id__in=self.tickets_ids, status="paid"
        ).count()

        self.assertEqual(self.order.status, "paid")
        self.assertEqual(tickets_count, 5)
