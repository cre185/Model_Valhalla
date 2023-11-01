from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from user import views as user_views
# Create your tests here.

class UserModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testuser",
        )
        user.save()
        self.client=Client()

    def test_login(self):
        # the correct case
        response=self.client.post(
            reverse(user_views.login),
            {
                "username":"testuser",
                "password":"testuser"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)
        # request with error password
        response=self.client.post(
            reverse(user_views.login),
            {
                "username":"testuser",
                "password":"error"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)
        # request with error username
        response=self.client.post(
            reverse(user_views.login),
            {
                "username":"error",
                "password":"testuser"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)
        # request with error json
        response=self.client.post(
            reverse(user_views.login),
            {
                "username":"testuser"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)

        response=self.client.post(
            reverse(user_views.login),
            {
                "password":"testuser"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)