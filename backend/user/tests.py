import datetime
import unittest

import pytz

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
            mobile="12345678901",
            email="someone@example.com"
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
        # test login with verify code
        VerifyMsg1 = VerifyMsg(
            mobile="12345678901",
            code="123456"
        )
        VerifyMsg1.save()
        response = self.client.post(
            '/user/login_with_verify_code',
            {
                "mobile": "12345678901",
                "code": "123456"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json_data['jwt'], None)
        # test login with wrong code
        response = self.client.post(
            '/user/login_with_verify_code',
            {
                "mobile": "12345678901",
                "code": "114514"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)
        # easter egg -- logout
        response = self.client.post(
            '/user/logout',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        # the correct case
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser2",
                "password": "testuser2",
                "mobile": "12345678902"
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
        # request with invalid mobile
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser3",
                "password": "testuser3",
                "mobile": "123456"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # request with same email
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser3",
                "password": "testuser3",
                "mobile": "12345678900",
                "email": "someone@example.com"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # request with invalid email
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser3",
                "password": "testuser3",
                "mobile": "12345678900",
                "email": "some"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # request with secret to become admin
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser3",
                "password": "testuser3",
                "mobile": "12345678900",
                "email": "some@exp.com",
                "secret": "TXNKvJ#1"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['is_admin'], True)


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
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 404)
        # test find user by name
        response = self.client.post(
            '/user/find_user_by_name',
            {
                "username": "testuser"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        # find user by wrong name
        response = self.client.post(
            '/user/find_user_by_name',
            {
                "username": "error"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test retrieve password
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
            '/user/retrieve_password',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['password'], "testuser")

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
        response = self.client.patch(
            '/user/update/1',
            {
                "username": "testuser2",
                "password": "testuser2",
                "mobile": "12345678902",
                "email": "some@exp.com"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        # request with wrong id
        response = self.client.patch(
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
        response = self.client.patch(
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
        # request another user's data
        response = self.client.patch(
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
        # request with same information
        response = self.client.patch(
            '/user/update/1',
            {
                "username": "testuser4",
                "mobile": "12345678902",
                "email": "some@exp.com"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['username'], "testuser4")
        self.assertEqual(json_data['mobile'], "12345678902")
        # request with invalid email
        response = self.client.patch(
            '/user/update/1',
            {
                "email": "error"
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test update avatar
        with open ("user/management/commands/static/avatar/avatar.png", "rb") as f:
            response = self.client.post(
                '/user/update_avatar',
                {
                    "file": f
                },
                HTTP_AUTHORIZATION=jwt,
                format="multipart"
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(User.objects.get(id=1).avatar, None)
        # test without file
        response = self.client.post(
            '/user/update_avatar',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
        # test update for a user with default avatar
        response = self.client.post(
            '/user/register',
            {
                "username": "testuser5",
                "password": "testuser5",
                "mobile": "12345678911"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser3",
                "password": "testuser3"
            },
            format="json"
        )
        json_data = response.json()
        jwt = json_data['jwt']
        with open ("user/management/commands/static/avatar/avatar.png", "rb") as f:
            response = self.client.post(
                '/user/update_avatar',
                {
                    "file": f
                },
                HTTP_AUTHORIZATION=jwt,
                format="multipart"
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(User.objects.get(id=2).avatar, None)
        
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
            '/user/subscribe_llm',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMSubscription.objects.all().count(), 1)
        # request with wrong llm_id
        response = self.client.post(
            '/user/subscribe_llm',
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
            '/user/subscribe_llm',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMSubscription.objects.all().count(), 0)
        # auto remove subscription when user is deleted
        response = self.client.post(
            '/user/subscribe_llm',
            {
                "llmId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMSubscription.objects.all().count(), 1)
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
        self.assertEqual(LLMSubscription.objects.all().count(), 0)
        # test subscribe dataset
        response = self.client.post(
            '/dataset/create',
            {
                "name": "testdataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/user/subscribe_dataset',
            {
                "datasetId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DatasetSubscription.objects.all().count(), 1)
        # request with wrong dataset_id
        response = self.client.post(
            '/user/subscribe_dataset',
            {
                "datasetId": 2
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # request again to unsubscribe
        response = self.client.post(
            '/user/subscribe_dataset',
            {
                "datasetId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DatasetSubscription.objects.all().count(), 0)

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
            '/user/subscribe_llm',
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
            '/user/list_llm_subscription/1',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['llms']), 1)
        self.assertEqual(response.status_code, 200)
        # request with wrong id
        response = self.client.get(
            '/user/list_llm_subscription/3',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test list dataset subscription
        response = self.client.post(
            '/dataset/create',
            {
                "name": "testdataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/user/subscribe_dataset',
            {
                "datasetId": 1
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DatasetSubscription.objects.all().count(), 1)
        response = self.client.get(
            '/user/list_dataset_subscription/1',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['datasets']), 1)
        self.assertEqual(response.status_code, 200)
        # request with wrong id
        response = self.client.get(
            '/user/list_dataset_subscription/3',
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


class VerifyModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testuser",
            mobile="12345678901"
        )
        user.save()
        self.client = APIClient()

    def test_verify_code(self):
        # send a verify code first
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
        # verify with wrong code
        response = self.client.post(
            '/user/verify_code',
            {
                "mobile": "12345678901",
                "code": "000000"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid code")
        self.assertEqual(response.status_code, 401)
        # verify with correct code
        verify_code = VerifyMsg.objects.get(mobile="12345678901").code
        response = self.client.post(
            '/user/verify_code',
            {
                "mobile": "12345678901",
                "code": verify_code
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        # send again to test resend
        response = self.client.post(
            '/user/send_message',
            {
                "mobile": "12345678901"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # send with wrong mobile
        response = self.client.post(
            '/user/send_message',
            {
                "mobile": "123123123"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test clear old code
        verifymsg = VerifyMsg.objects.create(
            mobile="12345678902",
            code="000000"
        )
        verifymsg.add_time = datetime.datetime.now()-datetime.timedelta(minutes=10)
        verifymsg.save()
        response = self.client.post(
            '/user/send_message',
            {
                "mobile": "12345678902"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VerifyMsg.objects.all().count(), 2)
        self.assertNotEqual(VerifyMsg.objects.get(mobile="12345678902").code, "000000")

    def test_verify_email(self):
        # send a verify code first
        response = self.client.post(
            '/user/send_email',
            {
                "email": "someone@example.com"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 201)
        # verify with wrong code
        response = self.client.post(
            '/user/verify_email',
            {
                "email": "someone@example.com",
                "code": "000000"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid code")
        self.assertEqual(response.status_code, 401)
        # verify with correct code
        verify_code = VerifyEmail.objects.get(email="someone@example.com").code
        response = self.client.post(
            '/user/verify_email',
            {
                "email": "someone@example.com",
                "code": verify_code
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        # send again to test resend
        response = self.client.post(
            '/user/send_email',
            {
                "email": "someone@example.com",
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # send with wrong email
        response = self.client.post(
            '/user/send_email',
            {
                "email": "someone"
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test clear old code
        verifyemail=VerifyEmail.objects.create(
            email="some@exp.com",
            code="000000"
        )
        verifyemail.add_time = datetime.datetime.now()-datetime.timedelta(minutes=10)
        verifyemail.save()
        response = self.client.post(
            '/user/send_email',
            {
                "email": "some@exp.com",
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VerifyEmail.objects.all().count(), 2)
        self.assertNotEqual(VerifyEmail.objects.get(email="some@exp.com").code, "000000")


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
        # emulate an expired jwt
        expiry = datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))
        payload = {"exp": expiry, "user_id": 1, "is_admin": False}
        secret = settings.JWT_SECRET
        jwt = pyjwt.encode(payload, secret, algorithm="HS256")
        # test jwt
        response = self.client.patch(
            '/user/update/1',
            {
                "username": "testuser2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json",
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_data['message'], "Token has expired.")


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
                "msg_type": "test type",
                "msg_content": {
                    "test": "test"
                }
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
        # send a message with file
        with open('user/management/commands/static/avatar/default.jpg', 'rb') as f:
            response = self.client.post(
                '/user/create_message',
                {
                    "target": 1,
                    "msg": "test message",
                    "msg_type": "test type",
                    "file": f
                },
                HTTP_AUTHORIZATION=jwt,
                format="multipart"
            )
            json_data = response.json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(json_data['message'], "ok")
            self.assertEqual(Msg.objects.all().count(), 3)
            self.assertEqual(MsgTarget.objects.all().count(), 4)
            self.assertNotEqual(Msg.objects.get(id=3).msg_file, None)
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
        # list message with invalid 
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
        # send with file
        with open('user/management/commands/static/avatar/default.jpg', 'rb') as f:
            response = self.client.post(
                '/user/create_message_to_admin',
                {
                    "msg": "test message",
                    "msg_type": "test type",
                    "file": f
                },
                HTTP_AUTHORIZATION=jwt,
                format="multipart"
            )
            json_data = response.json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(json_data['message'], "ok")
            self.assertEqual(Msg.objects.all().count(), 2)
            self.assertEqual(MsgTarget.objects.all().count(), 4)
            self.assertNotEqual(Msg.objects.get(id=2).msg_file, None)
