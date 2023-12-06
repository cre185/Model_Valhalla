from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ranking import models as ranking
from testing import models as testing
from utils.admin_required import admin_required
from utils.jwt import login_required

from .models import *
from .serializers import *

# Create your views here.


class createView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @login_required
    def post(self, request):
        request.data['author'] = request.user.id
        headers = self.create(request)
        data = Dataset.objects.get(id=headers.data['id'])
        for llm in testing.LLMs.objects.all():
            ranking.Credit.objects.create(LLM=llm, dataset=data, credit=None)
            if data.subjective:
                ranking.SubjectiveCredit.objects.create(
                    LLM=llm, dataset=data, credit_list=[])
        return Response({"message": "ok",
                         "datasetId": headers.data['id']},
                        status=status.HTTP_201_CREATED)


class uploadView(APIView):
    @login_required
    def post(self, request):
        target = Dataset.objects.get(id=request.data['id'])
        if not target:
            return Response({"message": "Invalid dataset id"},
                            status=status.HTTP_400_BAD_REQUEST)
        dict = request.FILES
        dataset = dict['file']
        target.data_file = dataset
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
        target = Dataset.objects.get(id=kwargs['id'])
        if not target:
            return Response({"message": "Invalid dataset id"},
                            status=status.HTTP_400_BAD_REQUEST)
        file = target.data_file
        response = Response(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(
            target.name)
        return response