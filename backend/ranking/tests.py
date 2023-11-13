from django.test import TestCase
from rest_framework.test import APIClient
from .models import Credit
from user.models import User
from dataset.models import Dataset
from testing.models import LLMs
# Create your tests here.

class CreditModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
        )
        user.save()
        self.client=APIClient()

    def test_update(self):
        # create two datasets and two LLMs first
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
            '/dataset/create', 
            {
                "name":"somedataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        dataset_id=response.json()['datasetId']
        response=self.client.post(
            '/dataset/create', 
            {
                "name":"somedataset2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        dataset_id2=response.json()['datasetId']
        response=self.client.post(
            '/testing/create', 
            {
                "name":"sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        llm_id=response.json()['llmId']
        response=self.client.post(
            '/testing/create', 
            {
                "name":"sometesting2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        llm_id2=response.json()['llmId']
        # update credits
        response=self.client.post(
            '/ranking/update', 
            {
                "datasetId":dataset_id,
                "llmId":llm_id,
                "credit":60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        changed_credit=Credit.objects.get(dataset_id=dataset_id, LLM_id=llm_id).credit
        self.assertEqual(changed_credit, 60)
        response=self.client.post(
            '/ranking/update', 
            {
                "datasetId":dataset_id2,
                "llmId":llm_id2,
                "credit":40,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        changed_credit=Credit.objects.get(dataset_id=dataset_id2, LLM_id=llm_id2).credit
        self.assertEqual(changed_credit, 40)
        # update with invalid credit
        response=self.client.post(
            '/ranking/update', 
            {
                "datasetId":dataset_id,
                "llmId":llm_id,
                "credit":-1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'], "Invalid credit")
        self.assertEqual(response.status_code, 400)
        response=self.client.post(
            '/ranking/update', 
            {
                "datasetId":dataset_id,
                "llmId":llm_id,
                "credit":101,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'], "Invalid credit")
        self.assertEqual(response.status_code, 400)
        # update with invalid datasetId
        response=self.client.post(
            '/ranking/update', 
            {
                "datasetId":114514,
                "llmId":llm_id,
                "credit":60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'], "Invalid datasetId or llmId")
        self.assertEqual(response.status_code, 400)