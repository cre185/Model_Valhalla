from .serializers import LLMsSerializer
from .models import LLMs
from dataset import models as dataset
from ranking import models as ranking
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from utils.jwt import login_required
from utils.admin_required import admin_required
from utils.auto_test import AutoTest

# Create your views here.

class createView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer

    def post(self, request):
        headers = self.create(request)
        llm = LLMs.objects.get(id=headers.data['id'])
        for data in dataset.Dataset.objects.all():
            ranking.Credit.objects.create(LLM=llm, dataset=data, credit=None)
        return Response({"message": "ok", "llmId": headers.data['id']}, status=status.HTTP_201_CREATED, headers=headers)
    
class deleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer

    @admin_required
    def delete(self, request, *args, **kwargs):
        try:
            instance = LLMs.objects.get(id=int(kwargs['id']))
            self.perform_destroy(instance)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid llm id"}, status=status.HTTP_400_BAD_REQUEST)
    
class testingView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        target = ranking.Credit.objects.all()
        if 'llmId' in data:
            target = target.filter(LLM_id=int(data['llmId']))
        if 'datasetId' in data:
            target = target.filter(dataset_id=int(data['datasetId']))
        if 'style' in data and data['style'] == 'fill':
            target = target.filter(credit__isnull=True)
        
        if target.count() == 0:
            return Response({"message": "No tests are carried out"}, status=status.HTTP_200_OK)
        for tar in target:
            dataset = tar.dataset
            llm = tar.LLM
            if not dataset.data_file:
                continue
            if not llm.api_url:
                continue
            autoTest = AutoTest()
            result = autoTest.whole_test(dataset.data_file.path, llm)
            correct_amount = result[0]
            amount = result[1]
            tar.credit = (100*correct_amount)/amount
            tar.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)