from django.test import TestCase
from rest_framework.test import APIClient
from .models import Dataset
# Create your tests here.

class DatasetModelTests(TestCase):
    def setUp(self):
        dataset=Dataset(
            name="testdataset",
        )
        dataset.save()
        self.client=APIClient()

    '''def test_upload(self):
        # the correct case
        response=self.client.post(
            '/dataset/upload', 
            {
                "name":"somedata",
            },
            format="json"
        )
        json_data=response.json()
        self.assertEqual(json_data['message'],"ok")
        self.assertEqual(response.status_code,201)'''