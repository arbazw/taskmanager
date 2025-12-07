from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class AuthTests(APITestCase):
    def test_user_can_register(self):
        url = reverse("register")
        data = {"username": "user1", "password": "pass12345"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_can_get_jwt_token(self):
        User.objects.create_user(username="user1", password="pass12345")
        url = reverse("token_obtain_pair")
        data = {"username": "user1", "password": "pass12345"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass12345")
        token_url = reverse("token_obtain_pair")
        response = self.client.post(token_url, {"username": "user1", "password": "pass12345"}, format="json")
        self.access = response.data["access"]
        self.auth_header = f"Bearer {self.access}"

    def test_create_task(self):
        url = reverse("task-list-create")
        data = {"title": "Test Task", "description": "Test description", "completed": False}
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.owner, self.user)

    def test_list_tasks_with_pagination(self):
        for i in range(15):
            Task.objects.create(title=f"Task {i}", description="d", completed=False, owner=self.user)
        url = reverse("task-list-create")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_filter_tasks_by_completed(self):
        Task.objects.create(title="T1", description="d", completed=True, owner=self.user)
        Task.objects.create(title="T2", description="d", completed=False, owner=self.user)
        url = reverse("task-list-create")
        response = self.client.get(url + "?completed=true", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data["results"]:
            self.assertTrue(item["completed"])

    def test_only_owner_can_update_task(self):
        task = Task.objects.create(title="T1", description="d", completed=False, owner=self.user)
        other = User.objects.create_user(username="user2", password="pass12345")
        token_url = reverse("token_obtain_pair")
        response = self.client.post(token_url, {"username": "user2", "password": "pass12345"}, format="json")
        other_access = response.data["access"]
        url = reverse("task-detail", args=[task.id])
        response = self.client.put(
            url,
            {"title": "Updated", "description": "d", "completed": True},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {other_access}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
