from django.test import TestCase
from rest_framework.test import APIClient

from dataset.models import Dataset
from testing.models import LLMs
from user.models import User

from .models import *

# Create your tests here.


class CreditModelTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        self.client = APIClient()

    def create_basics(self):
        # create two datasets and two LLMs, can be
        # used in other tests
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
            '/dataset/create',
            {
                "name": "somedataset",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        dataset_id = response.json()['datasetId']
        response = self.client.post(
            '/dataset/create',
            {
                "name": "somedataset2",
                "subjective": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        dataset_id2 = response.json()['datasetId']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        llm_id = response.json()['llmId']
        response = self.client.post(
            '/testing/create',
            {
                "name": "sometesting2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        llm_id2 = response.json()['llmId']
        return jwt, dataset_id, dataset_id2, llm_id, llm_id2

    def test_update(self):
        jwt, dataset_id, dataset_id2, llm_id, llm_id2 = self.create_basics()
        # update credits
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        changed_credit = Credit.objects.get(
            dataset_id=dataset_id, LLM_id=llm_id).credit
        self.assertEqual(changed_credit, 60)
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id2,
                "llmId": llm_id2,
                "credit": 40,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        changed_credit = Credit.objects.get(
            dataset_id=dataset_id2, LLM_id=llm_id2).credit
        self.assertEqual(changed_credit, 40)
        # update again to test average credit
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id2,
                "llmId": llm_id2,
                "credit": 70,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        changed_credit = Credit.objects.get(
            dataset_id=dataset_id2, LLM_id=llm_id2).credit
        self.assertEqual(changed_credit, 55)
        # update with invalid credit
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": -1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credit")
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 101,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credit")
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": "error",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # update with invalid datasetId
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": 114514,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid datasetId or llmId")
        self.assertEqual(response.status_code, 400)
        # update objective dataset as a user
        user2 = User(
            username="testuser2",
            password="testpassword",
            mobile="12345678902",
        )
        user2.save()
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser2",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 0,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def test_list(self):
        jwt, dataset_id, dataset_id2, llm_id, llm_id2 = self.create_basics()
        # list credits
        response = self.client.get(
            '/ranking/list',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data['data']), 4)
        self.assertEqual(json_data['data'][0]['dataset'], dataset_id)
        for i in range(4):
            self.assertEqual(json_data['data'][i]['credit'], None)
        # update credits
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id2,
                "llmId": llm_id2,
                "credit": 40,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        # list credits again
        response = self.client.get(
            '/ranking/list',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['data'][0]['credit'], 60)
        self.assertEqual(json_data['data'][1]['credit'], None)
        self.assertEqual(json_data['data'][2]['credit'], None)
        self.assertEqual(json_data['data'][3]['credit'], 40)
        # test list selected credit
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "datasetId": dataset_id,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['data'][0]['credit'], 60)
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "llmId": llm_id,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['data'][0]['credit'], 60)

    def test_retrieve(self):
        # the correct case
        jwt, dataset_id, dataset_id2, llm_id, llm_id2 = self.create_basics()
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/retrieve',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(json_data['credit'], 60)
        self.assertEqual(response.status_code, 200)
        # test retrieve with invalid datasetId
        response = self.client.post(
            '/ranking/retrieve',
            {
                "datasetId": 114514,
                "llmId": llm_id,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def test_clear(self):
        jwt, dataset_id, dataset_id2, llm_id, llm_id2 = self.create_basics()
        # update credits
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id2,
                "llmId": llm_id2,
                "credit": 40,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        # clear credits again
        response = self.client.post(
            '/ranking/clear',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Credit.objects.get(
                dataset_id=dataset_id,
                LLM_id=llm_id).credit,
            None)
        # test clear with invalid datasetId
        response = self.client.post(
            '/ranking/clear',
            {
                "datasetId": 114514,
                "llmId": llm_id,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def test_average(self):
        # init credits first
        jwt, dataset_id, dataset_id2, llm_id, llm_id2 = self.create_basics()
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id2,
                "llmId": llm_id,
                "credit": 40,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id2,
                "credit": 80,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        # test average for one llm
        response = self.client.get(
            '/ranking/average/1',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['average'], 50.00)
        # test average for all llms
        response = self.client.get(
            '/ranking/average_list',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data['data']), 2)
        self.assertEqual(json_data['data'][1], 80.00)
        # test average for invalid llm
        response = self.client.get(
            '/ranking/average/114514',
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def testlistselected(self):
        jwt, dataset_id, dataset_id2, llm_id, llm_id2 = self.create_basics()
        # update credits
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
                "credit": 60,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/update',
            {
                "datasetId": dataset_id2,
                "llmId": llm_id2,
                "credit": 40,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        # list selected credits
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "datasetId": dataset_id,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 2)
        self.assertEqual(json_data['data'][0]['credit'], 60)
        self.assertEqual(json_data['data'][1]['credit'], None)
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "llmId": llm_id2,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 2)
        self.assertEqual(json_data['data'][0]['credit'], None)
        self.assertEqual(json_data['data'][1]['credit'], 40)
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "datasetId": dataset_id,
                "llmId": llm_id,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(len(json_data['data']), 1)
        self.assertEqual(json_data['data'][0]['credit'], 60)
        # test list selected credit with invalid id
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "datasetId": 114514,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/ranking/list_selected_credit',
            {
                "llmId": 114514,
            },
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)


class CommentTests(TestCase):
    def setUp(self):
        user = User(
            username="testuser",
            password="testpassword",
            mobile="12345678901",
            is_admin=True,
        )
        user.save()
        dataset = Dataset(
            name="somedataset",
        )
        dataset.save()
        llm = LLMs(
            name="sometesting",
        )
        llm.save()
        self.client = APIClient()

    def test_comment(self):
        response = self.client.post(
            '/user/login',
            {
                "username": "testuser",
                "password": "testpassword",
            },
            format="json"
        )
        jwt = response.json()['jwt']
        # the correct comment
        response = self.client.post(
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "sometext",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(DatasetComment.objects.get(id=1).comment, "sometext")
        response = self.client.post(
            '/ranking/comment',
            {
                "llm": 1,
                "comment": "sometext",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(LLMComment.objects.get(id=1).comment, "sometext")
        # comment with empty comment
        response = self.client.post(
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # comment with too long comment
        response = self.client.post(
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "a" * 1001,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        # comment on llm with too long comment
        response = self.client.post(
            '/ranking/comment',
            {
                "llm": 1,
                "comment": "a" * 1001,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def test_listcomment(self):
        # test dataset comment
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
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "sometext",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "sometext2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.get(
            '/ranking/dataset_comment/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data['data']), 2)
        self.assertEqual(json_data['data'][0]['comment'], "sometext")
        self.assertEqual(json_data['data'][1]['comment'], "sometext2")
        # test llm comment
        response = self.client.post(
            '/ranking/comment',
            {
                "llm": 1,
                "comment": "sometext",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/comment',
            {
                "llm": 1,
                "comment": "sometext2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.get(
            '/ranking/llm_comment/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data['data']), 2)
        self.assertEqual(json_data['data'][0]['comment'], "sometext")
        self.assertEqual(json_data['data'][1]['comment'], "sometext2")
        # test comment with invalid datasetId
        response = self.client.get(
            '/ranking/dataset_comment/114514',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        response = self.client.get(
            '/ranking/llm_comment/114514',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)

    def testlikecomment(self):
        # test dataset comment
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
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "sometext",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/comment',
            {
                "dataset": 1,
                "comment": "sometext2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(DatasetComment.objects.all().count(), 2)
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(DatasetLike.objects.filter(comment_id=1).count(), 1)
        response = self.client.get(
            '/ranking/dataset_comment/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['data'][0]['like'], 1)
        # remove like
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(DatasetLike.objects.filter(comment_id=1).count(), 0)
        # add a dislike
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 1,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(DatasetLike.objects.filter(comment_id=1).count(), 1)
        self.assertEqual(DatasetLike.objects.get(comment_id=1).dislike, True)
        # change it directly to like and change it back
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 1,
                "dislike": False,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(DatasetLike.objects.get(comment_id=1).dislike, False)
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 1,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(DatasetLike.objects.get(comment_id=1).dislike, True)
        # remove dislike
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 1,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(DatasetLike.objects.filter(comment_id=1).count(), 0)
        # test llm comment
        response = self.client.post(
            '/ranking/comment',
            {
                "llm": 1,
                "comment": "sometext",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        response = self.client.post(
            '/ranking/comment',
            {
                "llm": 1,
                "comment": "sometext2",
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        self.assertEqual(LLMComment.objects.all().count(), 2)
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMLike.objects.filter(comment_id=1).count(), 1)
        response = self.client.get(
            '/ranking/llm_comment/1',
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['data'][0]['like'], 1)
        # remove like
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 1,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(LLMLike.objects.filter(comment_id=1).count(), 0)
        # add a dislike
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 1,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMLike.objects.filter(comment_id=1).count(), 1)
        self.assertEqual(LLMLike.objects.get(comment_id=1).dislike, True)
        # change it directly to like and change it back
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 1,
                "dislike": False,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMLike.objects.get(comment_id=1).dislike, False)
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 1,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LLMLike.objects.get(comment_id=1).dislike, True)
        # remove dislike
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 1,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(LLMLike.objects.filter(comment_id=1).count(), 0)
        # test like with invalid id
        response = self.client.post(
            '/ranking/like_llm_comment',
            {
                "id": 114514,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/ranking/like_dataset_comment',
            {
                "id": 114514,
                "dislike": True,
            },
            HTTP_AUTHORIZATION=jwt,
            format="json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
