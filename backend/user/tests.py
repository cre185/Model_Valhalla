from django.test import TestCase, Client
from django.urls import reverse
from .models import User, VerifyMsg
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

    def test_register(self):
        # the correct case
        response=self.client.post(
            reverse(user_views.register),
            {
                "username":"testuser2",
                "password":"testuser2",
                "mobile":"12345678901"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)
        # request with same username
        response=self.client.post(
            reverse(user_views.register),
            {
                "username":"testuser",
                "password":"testuser",
                "mobile":"12345678900"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Username already been used")
        self.assertEqual(response.status_code,400)
        # request with invalid username
        response=self.client.post(
            reverse(user_views.register),
            {
                "username":"short",
                "password":"testuser",
                "mobile":"12345678900"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Username is invalid")
        self.assertEqual(response.status_code,400)
        # request with invalid password
        response=self.client.post(
            reverse(user_views.register),
            {
                "username":"testuser3",
                "password":"!@#$%^&*()",
                "mobile":"12345678900"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Password is invalid")
        self.assertEqual(response.status_code,400)
        # request with same mobile
        response=self.client.post(
            reverse(user_views.register),
            {
                "username":"testuser3",
                "password":"testuser3",
                "mobile":"12345678901"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Mobile already been used")
        self.assertEqual(response.status_code,400)

    def test_logout(self):
        # logout without login
        response=self.client.get(
            reverse(user_views.logout),
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"User must be authorized.")
        self.assertEqual(response.status_code,401)
        # login first to get jwt
        response=self.client.post(
            reverse(user_views.login),
            {
                "username":"testuser",
                "password":"testuser"
            },
            content_type="application/json"
        )
        json_data=response.json()
        jwt=json_data['jwt']
        # logout with jwt
        response=self.client.get(
            reverse(user_views.logout),
            content_type="application/json",
            HTTP_AUTHORIZATION=jwt
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)

class VerifyMsgModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testuser",
            mobile="12345678901"
        )
        user.save()
        self.client=Client()

    def test_verify(self):
        # send a verify code first
        response=self.client.post(
            reverse(user_views.send_message),
            {
                "mobile":"12345678902"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)
        # verify with wrong code
        response=self.client.post(
            reverse(user_views.verify_code),
            {
                "mobile":"12345678902",
                "code":"000000"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid code")
        self.assertEqual(response.status_code,401)
        # verify with correct code
        verify_code=VerifyMsg.objects.get(mobile="12345678902").code
        response=self.client.post(
            reverse(user_views.verify_code),
            {
                "mobile":"12345678902",
                "code":verify_code
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)
    
    def test_login_with_verify_code(self):
        # login with verify code
        response=self.client.post(
            reverse(user_views.send_message),
            {
                "mobile":"12345678901"
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)
        verify_code=VerifyMsg.objects.get(mobile="12345678901").code
        response=self.client.post(
            reverse(user_views.login_with_verify_code),
            {
                "mobile":"12345678901",
                "code":verify_code
            },
            content_type="application/json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)