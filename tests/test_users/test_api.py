from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class TestCreateUserView(TestCase):
    def test_success_create(self):
        data = {
            "name": "Brandon Sanderson",
            "email": "elantris@gmail.com",
            "password": "Test1234!",
            "password2": "Test1234!",
        }
        response = self.client.post(reverse("register"), data=data)

        user_exists = UserModel.objects.filter(email=data["email"]).exists()

        self.assertTrue(user_exists)
        self.assertEqual(response.status_code, 201)


class TestCreateTokenView(TestCase):
    def setUp(self):
        user = UserModel.objects.create(name="Dan Simmons", email="hyperion@gmail.com")
        user.set_password("Test1234!")
        user.save()

    def test_success_authentication(self):
        data = {"username": "hyperion@gmail.com", "password": "Test1234!"}

        response = self.client.post(reverse("login"), data=data)

        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials(self):
        data = {"username": "dallas@gmail.com", "password": "Test1234!"}

        response = self.client.post(reverse("login"), data=data)

        self.assertEqual(response.status_code, 400)
