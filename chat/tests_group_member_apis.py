from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User, GroupMember


class TestUserAPIView(APITestCase):
    """
    Test Cases for GroupMember model to support search member, Add/view/delete member to group operations.
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

    def create_test_users(self):
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

    def test_should_serach_all_members(self):
        self.non_admin_authentication()
        self.create_test_users()
        response = self.client.get(reverse("search-member"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("users")), 4)

    def test_should_serach_members_with_username(self):
        self.non_admin_authentication()
        self.create_test_users()
        response = self.client.get('/chat/search-member?username=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("users")), 4)

    def test_should_add_member_to_group(self):
        self.non_admin_authentication()
        self.create_test_users()
        previous_count = GroupMember.objects.all().count()
        sample_request = {
            "group": 1,
            "member": 3
        }
        response = self.client.post(reverse("add-group-member"), sample_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get("success"))
        self.assertEqual(GroupMember.objects.all().count(), previous_count + 1)

    def test_should_return_group_members(self):
        self.non_admin_authentication()
        self.create_test_users()
        sample_request = {
            "group": 1,
            "member": 3
        }
        self.client.post(reverse("add-group-member"), sample_request, format="json")
        response = self.client.get("/chat/view-group-member?group_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("group_details")[0].get("group_id"), 1)
        self.assertEqual(len(response.data.get("group_details")[0].get("member_details")), 2)

    def test_should_remove_member_to_group(self):
        self.non_admin_authentication()
        self.create_test_users()
        previous_count = GroupMember.objects.all().count()
        sample_request = {
            "group": 1,
            "member": 3
        }
        self.client.post(reverse("add-group-member"), sample_request, format="json")
        self.assertEqual(GroupMember.objects.all().count(), previous_count + 1)
        response = self.client.delete(reverse("remove-group-member"), sample_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(GroupMember.objects.count(), previous_count)
