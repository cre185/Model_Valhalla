from .serializers import *
from .models import *
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
from utils.auto_test import *
from utils.elo_rating import *

# Create your views here.

class createView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer

    @login_required
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
        
class updateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer
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
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer
    lookup_field = "id"
    
    @login_required
    def get(self, request, *args, **kwargs):
        result = self.retrieve(request, *args, **kwargs)
        data = result.data
        data['message'] = 'ok'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)
    
class listView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer
    
    def get(self, request, *args, **kwargs):
        result = self.list(request, *args, **kwargs)
        data = result.data
        for i in range(len(data)):
            data[i]['add_time'] = data[i]['add_time'].split('T')[0]
        return Response({'message': 'ok', 'data': data}, status=status.HTTP_200_OK)

class testingView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        target = ranking.Credit.objects.filter(subjective=False)
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
            autoTest = AutoTest(llm)
            result = autoTest.whole_test(dataset.data_file.path)
            correct_amount = result[0]
            amount = result[1]
            tar.credit = (100*correct_amount)/amount
            tar.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

class battleMatchView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=int(data['llmId']))
            all_others = LLMs.objects.exclude(id=llm.id)
            if all_others.count() == 0:
                return Response({"message": "No other llms"}, status=status.HTTP_200_OK)
            nearest = all_others[0]
            for other in all_others:
                if abs(other.elo_credit - llm.elo_credit) < abs(nearest.elo_credit - llm.elo_credit):
                    nearest = other
            return Response({"message": "ok", "llmId": nearest.id}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
        
class generateView(APIView):  
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=int(data['llmId']))
            # todo: return the generate result
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

class battleResultView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        if 'llmId1' not in data or 'llmId2' not in data or 'result' not in data:
            return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            llm1 = LLMs.objects.get(id=int(data['llmId1']))
            llm2 = LLMs.objects.get(id=int(data['llmId2']))
            if llm1.id == llm2.id:
                return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
            if int(data['result']) not in [-1, 0, 1]:
                return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
            sa = (int(data['result'])+1.0)/2
            elo = EloRating()
            llm1.elo_credit, llm2.elo_credit=elo.cal_result(llm1.elo_credit, llm2.elo_credit, sa)
            llm1.save()
            llm2.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
    
class generateView(APIView):  
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=int(data['llmId']))
            autotest = AutoTest(llm)
            ans = autotest.call_api(data['prompt'])
            return Response({"message": "ok", "content": ans}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)