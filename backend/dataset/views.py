import os
from uuid import uuid4

from django.db import transaction
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ranking import models as ranking
from testing import models as testing
from utils.admin_required import admin_required
from utils.jwt import login_required
from utils.verify_dataset import *

from .models import *
from .serializers import *

# Create your views here.


class createView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @login_required
    def post(self, request):
        request.data['author'] = request.user.id
        request.data['content_size'] = 0
        headers = self.create(request)
        target = Dataset.objects.get(id=headers.data['id'])
        for llm in testing.LLMs.objects.all():
            ranking.Credit.objects.create(LLM=llm, dataset=target, credit=None)
        dataset = request.FILES.get('file')
        if not dataset:
            return Response({"message": "ok",
                         "datasetId": headers.data['id']},
                        status=status.HTTP_201_CREATED)
        # rename file
        dataset_name = str(target.id) + '_' + uuid4().hex + '.csv'
        content = dataset.read().decode('utf-8')
        try:
            target.subjective, target.content_size = verify_dataset(content)
        except Exception:
            return Response({"message": "Invalid dataset file"},
                            status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            # remove old file
            if target.data_file:
                try:
                    old_file_path = target.data_file.path
                    if os.path.isfile(old_file_path):
                        os.remove(old_file_path)
                        target.data_file.save(dataset_name, dataset)
                        target.save()
                except Exception:
                    return Response({"message": "Upload failed, please try again later."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                target.data_file.save(dataset_name, dataset)
                target.save()
        return Response({"message": "ok",
                         "datasetId": headers.data['id']},
                        status=status.HTTP_201_CREATED)


class uploadView(APIView):
    @login_required
    def post(self, request):
        try:
            if 'id' in request.data:
                target = Dataset.objects.get(id=request.data['id'])
            else:
                target = Dataset.objects.get(name=request.data['name'])
        except BaseException:
            return Response({"message": "Invalid dataset"},
                            status=status.HTTP_400_BAD_REQUEST)
        dataset = request.FILES.get('file')
        if not dataset:
            return Response({"message": "Invalid dataset file"},
                            status=status.HTTP_400_BAD_REQUEST)
        # rename file
        dataset_name = str(target.id) + '_' + uuid4().hex + '.csv'
        content = dataset.read().decode('utf-8')
        try:
            target.subjective, target.content_size = verify_dataset(content)
        except Exception:
            return Response({"message": "Invalid dataset file"},
                            status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            # remove old file
            if target.data_file:
                try:
                    old_file_path = target.data_file.path
                    if os.path.isfile(old_file_path):
                        os.remove(old_file_path)
                        target.data_file.save(dataset_name, dataset)
                        target.save()
                except Exception:
                    return Response({"message": "Upload failed, please try again later."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                target.data_file.save(dataset_name, dataset)
                target.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class deleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @admin_required
    def delete(self, request, *args, **kwargs):
        try:
            instance = Dataset.objects.get(id=int(kwargs['id']))
            self.perform_destroy(instance)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid dataset id"},
                            status=status.HTTP_400_BAD_REQUEST)


class updateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = "id"

    @admin_required
    def put(self, request, *args, **kwargs):
        result = self.update(request, *args, **kwargs)
        data = result.data
        data['message'] = 'ok'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)

    @admin_required
    def patch(self, request, *args, **kwargs):
        result = self.partial_update(request, *args, **kwargs)
        data = result.data
        data['message'] = 'ok'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)


class retrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        result = self.retrieve(request, *args, **kwargs)
        data = result.data
        data['message'] = 'ok'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)


class listView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    def get(self, request, *args, **kwargs):
        result = self.list(request, *args, **kwargs)
        data = result.data
        for i in range(len(data)):
            data[i]['add_time'] = data[i]['add_time'].split('T')[0]
        return Response({'message': 'ok', 'data': data},
                        status=status.HTTP_200_OK)


class downloadView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            target = Dataset.objects.get(id=kwargs['id'])
            file = target.data_file
            response = Response(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(
                target.name)
            return response
        except BaseException:
            return Response({"message": "Invalid dataset id"},
                            status=status.HTTP_400_BAD_REQUEST)


class updateTagView(APIView):
    @login_required
    def post(self, request):
        try:
            target = Dataset.objects.get(id=request.data['id'])
            target.tag = request.data['tag']
            target.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid dataset id"},
                            status=status.HTTP_400_BAD_REQUEST)


class previewView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            target = Dataset.objects.get(id=kwargs['id'])
            file = target.data_file
            content = file.read().decode('utf-8')
            data, subjective = get_first_10_rows(content)
            response = Response({'message': 'ok', 'data': data, 'subjective': subjective},
                                status=status.HTTP_200_OK)
            return response
        except BaseException:
            return Response({"message": "Invalid dataset id"},
                            status=status.HTTP_400_BAD_REQUEST)
