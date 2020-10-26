from datetime import datetime, timedelta
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from events.models import Event
from tickets.integrations.payment.payment import PaymentResult
from tickets.models import Order, Ticket

UserModel = get_user_model()


class TestOrderViewSet(TestCase):
    def setUp(self):
        future_date = datetime.now() + timedelta(days=10)
        self.event = Event.objects.create(
            name="Powerwolf in Wroclaw",
            event_date=future_date,
            place="Wroclaw",
            description="lorem ipsum",
        )
        data = {"price": 130, "amount": 1000, "ticket_type": "regular"}
        self.event.create_tickets(data)

        user = UserModel.objects.create_user(
            name="test test", password="Test1234!", email="test@gmail.com"
        )
        self.user = UserModel.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        data = {"amount": 5, "event_id": self.event.id, "ticket_type": "regular"}
        response = self.client.post(reverse("orders-list"), data=data)

        order_exists = Order.objects.filter(event=self.event).exists()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(order_exists)

    def test_create_without_enough_tickets(self):
        data = {"amount": 5, "event_id": self.event.id, "ticket_type": "vip"}
        response = self.client.post(reverse("orders-list"), data=data)

        order_exists = Order.objects.filter(event=self.event).exists()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(order_exists)

    def test_create_event_does_not_exist(self):
        data = {"amount": 5, "event_id": uuid4(), "ticket_type": "vip"}
        response = self.client.post(reverse("orders-list"), data=data)

        order_exists = Order.objects.filter(event=self.event).exists()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(order_exists)

    @patch(
        "tickets.models.PaymentGateway.charge", return_value=PaymentResult("100", "EUR")
    )
    def test_make_payment(self, mock):
        order = Order.objects.create(event=self.event, owner=self.user)
        tickets = Ticket.objects.filter(event=self.event)
        tickets_ids = [ticket.id for ticket in tickets][:2]
        order.attach_tickets(tickets_ids)

        data = {"amount": 260, "currency": "EUR", "token": "loremipsum"}
        response = self.client.post(
            reverse("orders-make_payment", kwargs={"pk": order.id}), data=data
        )

        order.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.status, "paid")

    @patch(
        "tickets.models.PaymentGateway.charge", return_value=PaymentResult("100", "EUR")
    )
    def test_make_payment_for_expired_reservation(self, mock):
        past_date = datetime.now() + timedelta(minutes=-20)
        order = Order.objects.create(event=self.event, owner=self.user)
        order.created_at = past_date
        order.save()

        tickets = Ticket.objects.filter(event=self.event)
        tickets_ids = [ticket.id for ticket in tickets][:2]
        order.attach_tickets(tickets_ids)

        data = {"amount": 260, "currency": "EUR", "token": "loremipsum"}
        response = self.client.post(
            reverse("orders-make_payment", kwargs={"pk": order.id}), data=data
        )

        order.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(order.status, "waiting")

    def test_get_orders_list(self):
        user_2 = UserModel.objects.create_user(
            name="test1 test1", password="Test1234!", email="test1@gmail.com"
        )

        Order.objects.bulk_create(
            [
                Order(event=self.event, owner=self.user),
                Order(event=self.event, owner=self.user),
                Order(event=self.event, owner=user_2),
            ]
        )

        response = self.client.get(reverse("orders-list",))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_order_detail(self):
        user_2 = UserModel.objects.create_user(
            name="test1 test1", password="Test1234!", email="test1@gmail.com"
        )
        order_1 = Order.objects.create(event=self.event, owner=self.user)
        order_2 = Order.objects.create(event=self.event, owner=user_2)

        response = self.client.get(reverse("orders-detail", kwargs={"pk": order_1.pk}))

        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("orders-detail", kwargs={"pk": order_2.pk}))

        self.assertEqual(response.status_code, 404)
