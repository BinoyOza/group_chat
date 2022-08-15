from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User


class TestUserAPIView(APITestCase):
    """
    Test cases for User model based APIs.
    Token based authentication is supported all over the APIs.
    APIs support operations for Create, Update, Login, Logout functionality.
    """

    def admin_authentication(self):
        user = User.objects.create(email="admin@gmail.com", username="admin", password="admin@1234", first_name="admin",
                                   is_admin=True, is_active=True)
        user.set_password("admin@1234")
        user.save()
        response = self.client.post(reverse("user-login"), {
            "username": "admin",
            "password": "admin@1234"
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data.get('token')}"
        )

    def non_admin_authentication(self):
        user = User.objects.create(email="test@gmail.com", username="test", password="admin@1234", first_name="test",
                                   is_admin=False, is_active=True)
        user.set_password("admin@1234")
        user.save()
        response = self.client.post(reverse("user-login"), {
            "username": "test",
            "password": "admin@1234"
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data.get('token')}"
        )

    def test_should_not_create_user_with_user_not_admin(self):
        self.non_admin_authentication()
        sample_request = {
            "email": "demo@gmail.com",
            "username": "demo",
            "password": "admin@1234",
            "first_name": "demo",
            "is_admin": False
        }
        response = self.client.post(reverse("user-create"), sample_request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_user_with_user_admin(self):
        self.admin_authentication()
        sample_request = {
            "email": "demo@gmail.com",
            "username": "demo",
            "password": "admin@1234",
            "first_name": "demo",
            "is_admin": False
        }
        response = self.client.post(reverse("user-create"), sample_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_user(self):
        self.admin_authentication()
        sample_request = {
            "email": "demo@gmail.com",
            "username": "demo",
            "password": "admin@1234",
            "first_name": "demo",
            "is_admin": False
        }
        self.client.post(reverse("user-create"), sample_request)
        update_request = {
            "first_name": "test",
        }
        response = self.client.put(reverse("user-update", kwargs={"pk": 2}), update_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("first_name"), "test")

    def test_should_logout(self):
        self.non_admin_authentication()
        response = self.client.get(reverse("user-logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
