from Model_Valhalla import settings
import unittest
from django.test import TestCase
from rest_framework.test import APIClient
from .models import *
from dataset.models import Dataset
from ranking.models import *
from user.models import User
import json
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

    def test_update(self):
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
        response=self.client.patch(
            '/testing/update/1', 
            {
                "name":"sometesting2",
                "description":"somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(LLMs.objects.get(id=1).name, "sometesting2")
        self.assertEqual(LLMs.objects.get(id=1).description, "somedescription")
        # llm does not exist
        response=self.client.patch(
            '/testing/update/2', 
            {
                "name":"sometesting2",
                "description":"somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 404)

    def test_retrieve(self):
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
                "description":"somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response=self.client.get(
            '/testing/retrieve/1', 
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMs.objects.count(), 1)
        self.assertEqual(json_data['name'], "sometesting")
        self.assertEqual(json_data['description'], "somedescription")
        # llm does not exist
        response=self.client.get(
            '/testing/retrieve/2', 
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 404)
    
    def test_list(self):
        response=self.client.get(
            '/testing/list'
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
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
                "description":"somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response=self.client.get(
            '/testing/list'
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 1)
        self.assertEqual(json_data['data'][0]['name'], "sometesting")

class BattleModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        llm1=LLMs(
            name="llm1",
        )
        llm1.save()
        llm2=LLMs(
            name="llm2",
        )
        llm2.save()
        llm3=LLMs(
            name="llm3",
        )
        llm3.save()
        self.client=APIClient()
    
    def test_battle(self):
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
            '/testing/battle_result',
            {
                "llm1":1,
                "llm2":2,
                "round":1,
                "result":json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner":1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LLMs.objects.get(id=1).elo_credit>1500, True)
        self.assertEqual(LLMs.objects.get(id=2).elo_credit<1500, True)
        response=self.client.post(
            '/testing/battle_result',
            {
                "llm1":2,
                "llm2":3,
                "round":1,
                "result":json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner":-1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LLMs.objects.get(id=2).elo_credit<1500, True)
        self.assertEqual(LLMs.objects.get(id=3).elo_credit>1500, True)
        # request with same llm  
        response=self.client.post(
            '/testing/battle_result',
            {
                "llm1":1,
                "llm2":1,
                "round":1,
                "result":json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner":-1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 400)
        # request with invalid llm
        response=self.client.post(
            '/testing/battle_result',
            {
                "llm1":1,
                "llm2":4,
                "round":1,
                "result":json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner":-1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 400)
        # test battle matching
        response=self.client.post(
            '/testing/battle_match',
            {
                "llmId":1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['llmId'], 3)
        response=self.client.post(
            '/testing/battle_match',
            {
                "llmId":2,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['llmId'], 3)

class BattleHistoryTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        llm1=LLMs(
            name="llm1",
        )
        llm1.save()
        llm2=LLMs(
            name="llm2",
        )
        llm2.save()
        llm3=LLMs(
            name="llm3",
        )
        llm3.save()
        self.client=APIClient()

    def test_history(self):
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
            '/testing/battle_result',
            {
                "llm1":1,
                "llm2":2,
                "round":1,
                "result":json.loads('[{"result1":"a","result2":"b","prompt":"c"}]'),
                "winner":1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LLMs.objects.get(id=1).elo_credit>1500, True)
        self.assertEqual(LLMs.objects.get(id=2).elo_credit<1500, True)
        self.assertEqual(BattleHistory.objects.count(), 1)
        json_record=BattleHistory.objects.get(id=1).result
        self.assertEqual(json_record[0]['result1'], 'a')
        response=self.client.post(
            '/testing/battle_result',
            {
                "llm1":2,
                "llm2":3,
                "round":1,
                "result":json.loads('[{"result1":"b","result2":"d","prompt":"c"}]'),
                "winner":1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(BattleHistory.objects.count(), 2)
        # test battle history
        response=self.client.post(
            '/testing/battle_history',
            {
                "llm":2,
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 2)
        json_record=json_data['data'][0]['result']
        self.assertEqual(json_record[0]['result1'], 'b')
        # test battle history with invalid llm
        response=self.client.post(
            '/testing/battle_history',
            {
                "llm":4,
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 400)

@unittest.skipUnless(settings.DEBUG == False, "skip ok")
class GenerateRelatedTests(TestCase):
    # Warning: the test case costs a lot of time, and will not be tested usually
    # Test carried out only when DEBUG is False
    def setUp(self):
        user=User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        llm1=LLMs(
            name="llm1",
        )
        llm1.save()
        llm2=LLMs(
            name="llm2",
            model_name="qwen_7b_chat",
        )
        llm2.save()
        dataset=Dataset(
            name="testdataset",
            data_file="static/data/ceval_select_lite.csv",
        )
        dataset.save()
        credit=Credit(
            LLM=llm1,
            dataset=dataset,
        )
        credit.save()
        credit=Credit(
            LLM=llm2,
            dataset=dataset,
        )
        credit.save()
        self.client=APIClient()

    def test_generate(self):
        # the correct case
        print('')
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
            '/testing/generate', 
            {
                "llmId":1,
                "prompt":"hello!",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        print('test_generate on model mistral_7b: ', json_data['content'])
        response=self.client.post(
            '/testing/generate', 
            {
                "llmId":2,
                "prompt":"hello!",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        print('test_generate on model qwen_7b_chat: ', json_data['content'])
        # test generate related with no llm
        response=self.client.post(
            '/testing/generate', 
            {
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 400) 

    def test_test(self):
        print('')
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
            '/testing/test', 
            {
                "llmId":1,
                "datasetId":1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        print('credit for model mistral_7b: ', Credit.objects.get(LLM_id=1, dataset_id=1).credit)
