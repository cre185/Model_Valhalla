from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, VerifyMsg
# Create your tests here.

class UserModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testuser",
        )
        user.save()
        self.client=APIClient()

    def test_login(self):
        # the correct case
        response=self.client.post(
            '/user/login', 
            {
                "username":"testuser",
                "password":"testuser"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)
        # request with error password
        response=self.client.post(
            '/user/login', 
            {
                "username":"testuser",
                "password":"error"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)
        # request with error username
        response=self.client.post(
            '/user/login', 
            {
                "username":"error",
                "password":"testuser"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)
        # request with error json
        response=self.client.post(
            '/user/login', 
            {
                "username":"testuser"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)

        response=self.client.post(
            '/user/login',
            {
                "password":"testuser"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid credentials")
        self.assertEqual(response.status_code,401)

    def test_register(self):
        # the correct case
        response=self.client.post(
            '/user/register',
            {
                "username":"testuser2",
                "password":"testuser2",
                "mobile":"12345678901"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)
        # request with same username
        response=self.client.post(
            '/user/register',
            {
                "username":"testuser",
                "password":"testuser",
                "mobile":"12345678900"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Username already been used")
        self.assertEqual(response.status_code,400)
        # request with invalid username
        response=self.client.post(
            '/user/register',
            {
                "username":"short",
                "password":"testuser",
                "mobile":"12345678900"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Username is invalid")
        self.assertEqual(response.status_code,400)
        # request with invalid password
        response=self.client.post(
            '/user/register',
            {
                "username":"testuser3",
                "password":"!@#$%^&*()",
                "mobile":"12345678900"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Password is invalid")
        self.assertEqual(response.status_code,400)
        # request with same mobile
        response=self.client.post(
            '/user/register',
            {
                "username":"testuser3",
                "password":"testuser3",
                "mobile":"12345678901"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Mobile already been used")
        self.assertEqual(response.status_code,400)

    def test_logout(self):
        # logout without login
        response=self.client.post(
            '/user/logout',
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"User must be authorized.")
        self.assertEqual(response.status_code,401)
        # login first to get jwt
        response=self.client.post(
            '/user/login',
            {
                "username":"testuser",
                "password":"testuser"
            },
            format="json"
        )
        json_data=response.json()
        jwt=json_data['jwt']
        # logout with jwt
        response=self.client.post(
            '/user/logout',
            HTTP_AUTHORIZATION=jwt,
            format="json",
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
        self.client=APIClient()

    def test_verify(self):
        # send a verify code first
        response=self.client.post(
            '/user/send_message',
            {
                "mobile":"12345678902"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)
        # verify with wrong code
        response=self.client.post(
            '/user/verify_code',
            {
                "mobile":"12345678902",
                "code":"000000"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"Invalid code")
        self.assertEqual(response.status_code,401)
        # verify with correct code
        verify_code=VerifyMsg.objects.get(mobile="12345678902").code
        response=self.client.post(
            '/user/verify_code',
            {
                "mobile":"12345678902",
                "code":verify_code
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)
    
    def test_login_with_verify_code(self):
        # login with verify code
        response=self.client.post(
            '/user/send_message',
            {
                "mobile":"12345678901"
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)
        verify_code=VerifyMsg.objects.get(mobile="12345678901").code
        response=self.client.post(
            '/user/login_with_verify_code',
            {
                "mobile":"12345678901",
                "code":verify_code
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)