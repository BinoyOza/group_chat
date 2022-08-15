from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User


class TestUserAPIView(APITestCase):
    """
    Test cases for Group Create and Get Group details APIs.
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

    def test_should_create_group_with_non_admin_user(self):
        self.non_admin_authentication()
        sample_request = {
            "name": "Demo Group",
            "about": "This is demo group for testing purpose."
        }
        response = self.client.post(reverse("group-create"), sample_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), "Demo Group")

    def test_should_get_groups_list(self):
        self.non_admin_authentication()
        sample_request = {
            "name": "Demo Group",
            "about": "This is demo group for testing purpose."
        }
        self.client.post(reverse("group-create"), sample_request, format="json")
        sample_request = {
            "name": "Test Group",
            "about": "This is demo group for testing purpose."
        }
        self.client.post(reverse("group-create"), sample_request, format="json")
        response = self.client.get(reverse("group-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(len(response.data.get('groups')), 2)

    def test_should_delete_group(self):
        self.non_admin_authentication()
        sample_request = {
            "name": "Demo Group",
            "about": "This is demo group for testing purpose."
        }
        self.client.post(reverse("group-create"), sample_request, format="json")
        response = self.client.delete(reverse("group-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_throw_error_on_delete_group_bad_request(self):
        self.non_admin_authentication()
        response = self.client.delete(reverse("group-delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
