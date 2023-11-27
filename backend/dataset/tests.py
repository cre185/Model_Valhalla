from django.test import TestCase
from rest_framework.test import APIClient

from user.models import User

from .models import Dataset

# Create your tests here.

class DatasetModelTests(TestCase):
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

    def test_delete(self):
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
        response=self.client.delete(
            '/dataset/delete/1', 
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(Dataset.objects.all()),0)
        # the dataset doesn't exist
        response=self.client.delete(
            '/dataset/delete/1', 
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code,400)

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
            '/dataset/create', 
            {
                "name":"somedataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response=self.client.patch(
            '/dataset/update/1', 
            {
                "name":"somedataset2",
                "description":"somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,200)
        self.assertEqual(Dataset.objects.get(id=1).name,"somedataset2")
        self.assertEqual(Dataset.objects.get(id=1).description,"somedescription")
        # the dataset doesn't exist
        response=self.client.patch(
            '/dataset/update/2', 
            {
                "name":"somedataset2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code,404)

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
            '/dataset/create', 
            {
                "name":"somedataset",
                "description":"somedescription",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response=self.client.get(
            '/dataset/retrieve/1', 
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(json_data['name'],"somedataset")
        self.assertEqual(json_data['description'],"somedescription")
        self.assertEqual(response.status_code,200)
        # the dataset doesn't exist
        response=self.client.get(
            '/dataset/retrieve/2', 
            format="json"
        )
        json_data=response.json()
        self.assertEqual(response.status_code,404)