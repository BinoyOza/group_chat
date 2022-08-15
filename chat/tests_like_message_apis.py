from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User


class TestUserAPIView(APITestCase):
    """
    Test Cases for like/view-like messages to a group.
    """

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

    def create_test_objects(self):
        user = User.objects.create(email="test1@gmail.com", username="test1", password="admin@1234", first_name="test1",
                                   is_admin=False, is_active=True)
        user.set_password("admin@1234")
        user.save()
        user = User.objects.create(email="test2@gmail.com", username="test2", password="admin@1234", first_name="test2",
                                   is_admin=False, is_active=True)
        user.set_password("admin@1234")
        user.save()
        user = User.objects.create(email="test3@gmail.com", username="test3", password="admin@1234", first_name="test3",
                                   is_admin=False, is_active=True)
        user.set_password("admin@1234")
        user.save()

        # Creating test group.
        sample_request = {
            "name": "Demo Group",
            "about": "This is demo group for testing purpose."
        }
        self.client.post(reverse("group-create"), sample_request, format="json")

        # Add members to group.
        sample_request = {
            "group": 1,
            "member": 3
        }
        self.client.post(reverse("add-group-member"), sample_request, format="json")

        sample_request = {
            "group": 1,
            "member": 2
        }
        self.client.post(reverse("add-group-member"), sample_request, format="json")

        # Send messages to the Group.
        sample_request = {
            "message": "This is an sample messagae to a group.",
            "sender": 1
        }
        self.client.post(reverse("send-message"), sample_request, format="json")
        sample_request = {
            "message": "This is an demo message to a group.",
            "sender": 2
        }
        self.client.post(reverse("send-message"), sample_request, format="json")
        sample_request = {
            "message": "Hi, how are you?",
            "sender": 2
        }
        self.client.post(reverse("send-message"), sample_request, format="json")

    def test_should_like_message(self):
        self.non_admin_authentication()
        self.create_test_objects()
        sample_request = {
            "message": 1,
            "member": 2
        }
        response = self.client.post(reverse("like-message"), sample_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get("like"))
        self.assertEqual((response.data.get("member_name")), "test2")

    def test_should_view_message_likes(self):
        self.non_admin_authentication()
        self.create_test_objects()
        sample_request = {
            "message": 1,
            "member": 2
        }
        self.client.post(reverse("like-message"), sample_request, format="json")
        sample_request = {
            "message": 1,
            "member": 3
        }
        self.client.post(reverse("like-message"), sample_request, format="json")
        response = self.client.get("/chat/view-message-likes?message_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("like_details")[0].get("message_id"), 1)
        self.assertEqual(len(response.data.get("like_details")[0].get("like_members")), 2)
