from django.test import TestCase
from rest_framework.test import APIClient
from .models import Dataset
from user.models import User
# Create your tests here.

class DatasetModelTests(TestCase):
    def setUp(self):
        user=User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
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
            '/dataset/create', 
            {
                "name":"somedataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(json_data['datasetId'],1)
        self.assertEqual(response.status_code,201)
        dataset=Dataset.objects.get(name="somedataset")
        self.assertEqual(dataset.author,User.objects.get(username="testuser"))
        # the name has already been used
        response=self.client.post(
            '/dataset/create', 
            {
                "name":"somedataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code,400)
