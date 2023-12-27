import json

from django.test import TestCase
from rest_framework.test import APIClient

from dataset.models import Dataset
from ranking.models import *
from user.models import User

from .models import *

# Create your tests here.


class LLMsModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        self.client = APIClient()

    def test_create(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
                "api_url": "http://test.com",
                "model_name": "testmodel",
                "api_RPM": 100,
                "official_website": "http://test.com",
                "description": "somedescription",
                "document_name": "testdocument",
                "document_website": "http://test.com",
                "license": "testlicense",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['llmId'], 1)
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(LLMs.objects.get(id=1).name, "sometesting")
        # name already exists
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LLMs.objects.count(), 1)
        # invalid RPM
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting2",
                "api_url": "http://test.com",
                "model_name": "testmodel",
                "api_RPM": 0,
                "official_website": "http://test.com",
                "description": "somedescription",
                "document_name": "testdocument",
                "document_website": "http://test.com",
                "license": "testlicense",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LLMs.objects.count(), 1)

    def test_delete(self):
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        # llm does not exist
        response = self.client.delete(
            '/testing/delete/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # the correct case
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(LLMs.objects.count(), 1)
        response = self.client.delete(
            '/testing/delete/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 0)

    def test_update(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.patch(
            '/testing/update/1',
            {
                "name": "sometesting2",
                "description": "somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(LLMs.objects.get(id=1).name, "sometesting2")
        self.assertEqual(LLMs.objects.get(id=1).description, "somedescription")
        # update with same name
        response = self.client.patch(
            '/testing/update/1',
            {
                "name": "sometesting2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(LLMs.objects.get(id=1).name, "sometesting2")
        llm2 = LLMs(
            name="sometesting3",
        )
        llm2.save()
        response = self.client.patch(
            '/testing/update/2',
            {
                "name": "sometesting2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # llm does not exist
        response = self.client.patch(
            '/testing/update/114514',
            {
                "name": "sometesting2",
                "description": "somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 404)

    def test_retrieve(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
                "description": "somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.get(
            '/testing/retrieve/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(json_data['name'], "sometesting")
        self.assertEqual(json_data['description'], "somedescription")
        # llm does not exist
        response = self.client.get(
            '/testing/retrieve/2',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        response = self.client.get(
            '/testing/list'
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
                "description": "somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.get(
            '/testing/list'
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 1)
        self.assertEqual(json_data['data'][0]['name'], "sometesting")

    def test_upload(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 1)
        with open('user/management/commands/static/logo/mistral_7b.png', 'rb') as f:
            response = self.client.post(
                '/testing/upload',
                {
                    "llmId": 1,
                    "file": f
                },
                HTTP_AUTHORIZATION=jwt,
                format="multipart"
            )
            json_data = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json_data['message'], "ok")
            self.assertNotEqual(LLMs.objects.get(id=1).logo, None)
        # llm does not exist
        with open('user/management/commands/static/logo/mistral_7b.png', 'rb') as f:
            response = self.client.post(
                '/testing/upload',
                {
                    "llmId": 2,
                    "file": f
                },
                HTTP_AUTHORIZATION=jwt,
                format="multipart"
            )
            json_data = response.json()
            self.assertEqual(response.status_code, 400)
        # file does not exist
        response = self.client.post(
            '/testing/upload',
            {
                "llmId": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)


class BattleModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        llm1 = LLMs(
            name="llm1",
        )
        llm1.save()
        self.client = APIClient()

    def test_battle(self):
        # test battle matching
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/battle_match',
            {
                "llmId": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "No other llms")
        llm2 = LLMs(
            name="llm2",
        )
        llm2.save()
        llm3 = LLMs(
            name="llm3",
        )
        llm3.save()
        response = self.client.post(
            '/testing/battle_match',
            {
                "llmId": 2,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        response = self.client.post(
            '/testing/battle_match',
            {
                "llmId": 4,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # test battle result
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 1,
                "llm2": 2,
                "round": 1,
                "result": json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LLMs.objects.get(id=1).elo_credit > 1500, True)
        self.assertEqual(LLMs.objects.get(id=2).elo_credit < 1500, True)
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 2,
                "llm2": 3,
                "round": 1,
                "result": json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner": -1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LLMs.objects.get(id=2).elo_credit < 1500, True)
        self.assertEqual(LLMs.objects.get(id=3).elo_credit > 1500, True)
        # request with same llm
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 1,
                "llm2": 1,
                "round": 1,
                "result": json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner": -1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # request with invalid llm
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 1,
                "llm2": 4,
                "round": 1,
                "result": json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner": -1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # now match again
        response = self.client.post(
            '/testing/battle_match',
            {
                "llmId": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['llmId'], 3)
        response = self.client.post(
            '/testing/battle_match',
            {
                "llmId": 2,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['llmId'], 3)

    def test_battle_history(self):
        llm2 = LLMs(
            name="llm2",
        )
        llm2.save()
        llm3 = LLMs(
            name="llm3",
        )
        llm3.save()
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 1,
                "llm2": 2,
                "round": 1,
                "result": json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        json_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LLMs.objects.get(id=1).elo_credit > 1500, True)
        self.assertEqual(LLMs.objects.get(id=2).elo_credit < 1500, True)
        self.assertEqual(BattleHistory.objects.count(), 1)
        json_record = BattleHistory.objects.get(id=1).result
        self.assertEqual(json_record[0]['result1'], 'a')
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 2,
                "llm2": 3,
                "round": 1,
                "result": json.loads('[{"result1":"b","result2":"d","prompt":"c"}]'),
                "winner": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        self.assertEqual(BattleHistory.objects.count(), 2)
        # request with invalid winner
        response = self.client.post(
            '/testing/battle_result',
            {
                "llm1": 2,
                "llm2": 3,
                "round": 1,
                "result": json.loads('[{"result1":"b","result2":"d","prompt":"c"}]'),
                "winner": 2,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json")
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BattleHistory.objects.count(), 2)
        # test battle history
        response = self.client.post(
            '/testing/battle_history',
            {
                "llm": 2,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 2)
        json_record = json_data['data'][0]['result']
        self.assertEqual(json_record[0]['result1'], 'b')
        # test battle history with invalid llm
        response = self.client.post(
            '/testing/battle_history',
            {
                "llm": 4,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)


# @unittest.skipUnless(settings.DEBUG == False, "skip ok")
class GenerateRelatedTests(TestCase):
    # Warning: the test case costs a lot of time, and will not be tested usually
    # Test carried out only when DEBUG is False
    def setUp(self):
        user = User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        llm1 = LLMs(
            name="llm1",
        )
        llm1.save()
        llm2 = LLMs(
            name="llm2",
            model_name="qwen_7b_chat",
        )
        llm2.save()
        dataset = Dataset(
            name="testdataset",
            data_file="user/management/commands/static/data/ceval_lite.csv",
        )
        dataset.save()
        credit = Credit(
            LLM=llm1,
            dataset=dataset,
        )
        credit.save()
        credit = Credit(
            LLM=llm2,
            dataset=dataset,
        )
        credit.save()
        self.client = APIClient()

    def test_generate(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/generate',
            {
                "llmId": 1,
                "prompt": "hello!",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        # print('test_generate on model mistral_7b: ', json_data['content'])
        response = self.client.post(
            '/testing/generate',
            {
                "llmId": 2,
                "prompt": "hello!",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        # print('test_generate on model qwen_7b_chat: ', json_data['content'])
        # test generate related with no llm
        response = self.client.post(
            '/testing/generate',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def test_test(self):
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        # the correct case
        response = self.client.post(
            '/testing/test',
            {
                "llmId": 1,
                "datasetId": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        credit1 = Credit.objects.get(id=1)
        # test with fill
        response = self.client.post(
            '/testing/test',
            {
                "style": "fill",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(
            Credit.objects.get(
                id=1).credit_list,
            credit1.credit_list)
        # test on all
        response = self.client.post(
            '/testing/test',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertNotEqual(
            Credit.objects.get(
                id=1).credit_list,
            credit1.credit_list)
        # test with all credit filtered
        response = self.client.post(
            '/testing/test',
            {
                "style": "fill",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "No tests are carried out")

    def test_stream_generate(self):
        # the correct case
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/testing/stream_generate',
            {
                "llmId": 1,
                "prompt": "hello!",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        text = ''
        for line in response.streaming_content:
            text += line.decode('utf-8')
        # print('stream generation complete: ', text)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(text, '')
        # test generate related with no llm
        response = self.client.post(
            '/testing/stream_generate',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(response.status_code, 400)
