import unittest

import jwt as pyjwt
from django.test import TestCase
from rest_framework.test import APIClient

from Model_Valhalla import settings

from .models import *

# Create your tests here.


class UserModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testuser",
        )
        user.save()
        self.client = APIClient()

    def test_login(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        # request with error password
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "error"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)
        # request with error username
        response = self.client.post(
            '/user/login',
            {
                "username": "error",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)
        # request with error json
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)

        response = self.client.post(
            '/user/login',
            {
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)

    def test_register(self):
        # the correct case
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser2",
                "password": "testuser2",
                "mobile": "12345678901"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        # request with same username
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser",
                "password": "testuser",
                "mobile": "12345678900"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Username already been used")
        self.assertEqual(response.status_code, 400)
        # request with invalid username
        response = self.client.post(
            '/user/register',
            {
                "username": "short",
                "password": "testuser",
                "mobile": "12345678900"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Username is invalid")
        self.assertEqual(response.status_code, 400)
        # request with invalid password
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser3",
                "password": "!@#$%^&*()",
                "mobile": "12345678900"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Password is invalid")
        self.assertEqual(response.status_code, 400)
        # request with same mobile
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser3",
                "password": "testuser3",
                "mobile": "12345678901"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Mobile already been used")
        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        # logout without login
        response = self.client.post(
            '/user/logout',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)
        # login first to get jwt
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        # logout with jwt
        response = self.client.post(
            '/user/logout',
            HTTP_AUTHORIZATION=jwt,
            format="json",
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)


class UserDataModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testuser",
            mobile="12345678901"
        )
        user.save()
        user2 = User(
            username="testtest",
            password="testtest",
            mobile="11122233344"
        )
        user2.save()
        self.client = APIClient()

    def test_retrieve(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.get(
            '/user/retrieve/1',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['username'], "testuser")
        self.assertEqual(json_data['mobile'], "12345678901")
        # request with wrong id
        response = self.client.get(
            '/user/retrieve/3',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.put(
            '/user/update/1',
            {
                "username": "testuser2",
                "password": "testuser2",
                "mobile": "12345678902"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        # request with wrong id
        response = self.client.put(
            '/user/update/3',
            {
                "username": "testuser2",
                "password": "testuser2",
                "mobile": "12345678902"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 404)
        # request with invalid username
        response = self.client.put(
            '/user/update/1',
            {
                "username": "short",
                "password": "testuser2",
                "mobile": "12345678902"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Username is invalid")
        self.assertEqual(response.status_code, 400)
        # unauthorized request
        response = self.client.put(
            '/user/update/1',
            {
                "username": "testuser2",
                "password": "testuser2",
                "mobile": "12345678902"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)
        # request another user's data
        response = self.client.put(
            '/user/update/2',
            {
                "username": "testuser3",
                "password": "testuser3",
                "mobile": "12345678903"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)
        # test partial update
        response = self.client.patch(
            '/user/update/1',
            {
                "username": "testuser4"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['username'], "testuser4")
        self.assertEqual(json_data['mobile'], "12345678902")

    def test_subscribe(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "testllm",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/user/subscribe',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.get(
                id=1).subscribed_llm.all()[0].name,
            "testllm")
        # request with wrong llm_id
        response = self.client.post(
            '/user/subscribe',
            {
                "llmId": 2
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # request again to unsubscribe
        response = self.client.post(
            '/user/subscribe',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.get(
                id=1).subscribed_llm.all().count(), 0)
        # auto remove subscription when user is deleted
        response = self.client.post(
            '/user/subscribe',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.get(
                id=1).subscribed_llm.all().count(), 1)
        user = User.objects.create(
            username="testuser2",
            password="testuser2",
            mobile="12345678902",
            is_admin=True)
        user.save()
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser2",
                "password": "testuser2"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.delete(
            '/user/delete/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subscription.objects.all().count(), 0)

    def test_sublist(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "testllm",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/user/subscribe',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            '/user/list_subscription/1',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['llms']), 1)
        self.assertEqual(response.status_code, 200)
        # request with wrong id
        response = self.client.get(
            '/user/list_subscription/3',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)


class UserAdminModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testuser",
            mobile="12345678901",
            is_admin=True
        )
        user.save()
        user2 = User(
            username="testtest",
            password="testtest",
            mobile="11122233344"
        )
        user2.save()
        user3 = User(
            username="testtest2",
            password="testtest2",
            mobile="11122233345"
        )
        user3.save()
        user4 = User(
            username="testtest3",
            password="testtest3",
            mobile="11122233346"
        )
        user4.save()
        self.client = APIClient()

    def test_delete(self):
        # the correct case for admin
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.delete(
            '/user/delete/4',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser3",
                "password": "testuser3"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)
        # delete others without admin
        response = self.client.post(
            '/user/login',
            {
                "username": "testtest",
                "password": "testtest"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.delete(
            '/user/delete/3',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)
        # delete with wrong id
        response = self.client.delete(
            '/user/delete/5',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)
        # unauthorized request
        response = self.client.delete(
            '/user/delete/2',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "User must be authorized.")
        self.assertEqual(response.status_code, 401)
        # delete self
        response = self.client.delete(
            '/user/delete/2',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/user/login',
            {
                "username": "testtest",
                "password": "testtest"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)


class VerifyMsgModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testuser",
            mobile="12345678901"
        )
        user.save()
        self.client = APIClient()

    def test_verify(self):
        # send a verify code first
        response = self.client.post(
            '/user/send_message',
            {
                "mobile": "12345678902"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 201)
        # verify with wrong code
        response = self.client.post(
            '/user/verify_code',
            {
                "mobile": "12345678902",
                "code": "000000"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid code")
        self.assertEqual(response.status_code, 401)
        # verify with correct code
        verify_code = VerifyMsg.objects.get(mobile="12345678902").code
        response = self.client.post(
            '/user/verify_code',
            {
                "mobile": "12345678902",
                "code": verify_code
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)

    def test_login_with_verify_code(self):
        # login with verify code
        response = self.client.post(
            '/user/send_message',
            {
                "mobile": "12345678901"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 201)
        verify_code = VerifyMsg.objects.get(mobile="12345678901").code
        response = self.client.post(
            '/user/login_with_verify_code',
            {
                "mobile": "12345678901",
                "code": verify_code
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)


@unittest.skipUnless(settings.DEBUG == False, "skip ok")
class JwtTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testuser",
            mobile="12345678901"
        )
        user.save()
        self.client = APIClient()

    def test_jwt_expire(self):
        # login first to get jwt
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        # test jwt
        import time
        time.sleep(2)
        response = self.client.post(
            '/user/logout',
            HTTP_AUTHORIZATION=jwt,
            format="json",
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        new_jwt = json_data['jwt']
        self.assertNotEqual(jwt, new_jwt)
        # test new_jwt is newer
        secret = settings.JWT_SECRET
        payload = pyjwt.decode(jwt, secret, algorithms=["HS256"])
        new_payload = pyjwt.decode(new_jwt, secret, algorithms=["HS256"])
        self.assertGreater(new_payload['exp'], payload['exp'])


class MsgModelTests(TestCase):
    def setUp(self):
        user1 = User(
            username="testuser",
            password="testuser",
            mobile="12345678901"
        )
        user1.save()
        user2 = User(
            username="testtest",
            password="testtest",
            mobile="11122233344",
            is_admin=True
        )
        user2.save()
        user3 = User(
            username="testtest2",
            password="testtest2",
            mobile="11122233345",
            is_admin=True
        )
        user3.save()
        self.client = APIClient()

    def test_create_message(self):
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        # send a message to user2
        response = self.client.post(
            '/user/create_message',
            {
                "target": [2],
                "msg": "test message",
                "msg_type": "test type"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(Msg.objects.all().count(), 1)
        self.assertEqual(MsgTarget.objects.all().count(), 1)
        # send a message to all users
        response = self.client.post(
            '/user/create_message',
            {
                "target": [1, 2],
                "msg": "test message",
                "msg_type": "test type"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(Msg.objects.all().count(), 2)
        self.assertEqual(MsgTarget.objects.all().count(), 3)
        # user2 send a message to all users
        response = self.client.post(
            '/user/login',
            {
                "username": "testtest",
                "password": "testtest"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.post(
            '/user/create_message',
            {
                "target": [1],
                "msg": "test message",
                "msg_type": "test type"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        response = self.client.post(
            '/user/create_message',
            {
                "target": [1, 2],
                "msg": "test message",
                "msg_type": "test type"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(Msg.objects.all().count(), 4)
        self.assertEqual(MsgTarget.objects.all().count(), 6)
        # test list message
        response = self.client.get(
            '/user/list_message',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data['msgs']), 3)
        # test check message
        response = self.client.post(
            '/user/check_message',
            {
                "id": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(MsgTarget.objects.get(id=1).read, True)
        response = self.client.get(
            '/user/list_message',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['msgs'][0]['read'], True)
        # test check of other user
        response = self.client.post(
            '/user/check_message',
            {
                "id": 3
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test another's check
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.post(
            '/user/check_message',
            {
                "id": 2
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/user/login',
            {
                "username": "testtest",
                "password": "testtest"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.get(
            '/user/list_message',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['msgs'][1]['read'], False)

    def test_to_admin(self):
        # login as user
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        # send a message to all admin
        response = self.client.post(
            '/user/create_message_to_admin',
            {
                "msg": "test message",
                "msg_type": "test type"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        response = self.client.post(
            '/user/login',
            {
                "username": "testtest",
                "password": "testtest"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        response = self.client.get(
            '/user/list_message',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(len(json_data['msgs']), 1)
