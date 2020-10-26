from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from events.models import Event

UserModel = get_user_model()


class TestEventManagementViewSet(TestCase):
    def setUp(self):
        user = UserModel.objects.create_superuser(
            name="test test", password="Test1234!", email="test@gmail.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.future_date_1 = datetime.now() + timedelta(days=+30)
        self.future_date_2 = datetime.now() + timedelta(days=+37)
        self.events = Event.objects.bulk_create(
            [
                Event(
                    name="Powerwolf in Wroclaw",
                    event_date=self.future_date_1,
                    place="Wroclaw",
                    description="lorem ipsum",
                ),
                Event(
                    name="Powerwolf in Wroclaw",
                    event_date=self.future_date_2,
                    place="Wroclaw",
                    description="lorem ipsum",
                ),
            ]
        )

    def test_get_event_list(self):
        response = self.client.get(reverse("admin_events-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.events))

    def test_get_event_detail(self):
        response = self.client.get(
            reverse("admin_events-detail", kwargs={"pk": self.events[0].id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.events[0].id))

    def test_update_event(self):
        response = self.client.patch(
            reverse("admin_events-detail", kwargs={"pk": self.events[0].id}),
            data={"place": "Warszawa"},
        )

        self.events[0].refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.events[0].place, "Warszawa")

    def test_create_event(self):
        data = {
            "name": "Michael Jackson Resurection",
            "event_date": self.future_date_1,
            "place": "Azeroth",
        }
        response = self.client.post(reverse("admin_events-list"), data=data)

        event_exist = Event.objects.filter(
            name=data["name"], event_date=data["event_date"], place=data["place"]
        ).exists()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(event_exist)

    def test_create_tickets_for_event(self):
        with patch("events.views.add_tickets.delay") as mock_task:
            data = {"ticket_type": "regular", "amount": 800, "price": 80}
            response = self.client.post(
                reverse("admin_events-create_tickets", kwargs={"pk": self.events[0].id}),
                data=data,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(mock_task.called)


class TestEventViewSet(TestCase):
    def setUp(self):
        user = UserModel.objects.create_user(
            name="test test", password="Test1234!", email="test@gmail.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.future_date_1 = datetime.now() + timedelta(days=+30)
        self.future_date_2 = datetime.now() + timedelta(days=+37)
        self.past_date_1 = datetime.now() + timedelta(days=+37)
        self.events = Event.objects.bulk_create(
            [
                Event(
                    name="Powerwolf in Wroclaw",
                    event_date=self.future_date_1,
                    place="Wroclaw",
                    description="lorem ipsum",
                ),
                Event(
                    name="Powerwolf in Wroclaw",
                    event_date=self.future_date_2,
                    place="Wroclaw",
                    description="lorem ipsum",
                ),
                Event(
                    name="Powerwolf in Wroclaw",
                    event_date=self.past_date_1,
                    place="Wroclaw",
                    description="lorem ipsum",
                ),
            ]
        )

    def test_get_event_list(self):
        response = self.client.get(reverse("events-list"))

        upcoming_events_count = Event.objects.filter(
            event_date__gt=datetime.now()
        ).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), upcoming_events_count)

    def test_get_event_detail(self):
        response = self.client.get(
            reverse("events-detail", kwargs={"pk": self.events[0].id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.events[0].id))
