from django.test import TestCase
from rest_framework.test import APIClient
from .models import LLMs
from user.models import User
from dataset.models import Dataset
from testing.models import LLMs
# Create your tests here.

class LLMsModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        self.client=APIClient()

    def test_create(self):
        # the correct case
        response=self.client.post(
            '/user/login',
            {
                "username":"testuser",
                "password":"testpassword",
            },
            format="json"
        )
        jwt=response.json()['jwt']
        response=self.client.post(
            '/testing/create', 
            {
                "name":"sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['llmId'], 1)
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(LLMs.objects.get(id=1).name, "sometesting")
        # name already exists
        response=self.client.post(
            '/testing/create', 
            {
                "name":"sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LLMs.objects.count(), 1)

    def test_delete(self):
        response=self.client.post(
            '/user/login',
            {
                "username":"testuser",
                "password":"testpassword",
            },
            format="json"
        )
        jwt=response.json()['jwt']
        # llm does not exist
        response=self.client.delete(
            '/testing/delete/1', 
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 400)
        # the correct case
        response=self.client.post(
            '/testing/create', 
            {
                "name":"sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(LLMs.objects.count(), 1)
        response=self.client.delete(
            '/testing/delete/1', 
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 0)
