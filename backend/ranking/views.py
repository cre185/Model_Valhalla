from utils.jwt import login_required
from utils.admin_required import admin_required
from .serializers import *
from .models import *
from dataset import models as dataset
from testing import models as testing
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# Create your views here.

class updateView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        dataset_id = data['datasetId']
        llm_id = data['llmId']
        try:
            d = dataset.Dataset.objects.get(id=dataset_id)
            if not d.subjective and not request.user.is_admin:
                return Response({"message": "User must be admin."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Invalid datasetId or llmId"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target = Credit.objects.get(dataset_id=dataset_id, LLM_id=llm_id)
            serializer = CreditSerializer(target, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "ok"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid credit"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Invalid datasetId or llmId"}, status=status.HTTP_400_BAD_REQUEST)
        
class listView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    
    def get(self, request):
        result = self.list(request)
        return Response({'message': 'ok', 'data': result.data}, status=status.HTTP_200_OK)
    
class retrieveView(APIView):
    def post(self, request):
        data = request.data
        dataset_id = data['datasetId']
        llm_id = data['llmId']
        try:
            target = Credit.objects.get(dataset_id=dataset_id, LLM_id=llm_id)
            return Response({"message": "ok", "credit": target.credit}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid datasetId or llmId"}, status=status.HTTP_400_BAD_REQUEST)
        
class clearView(APIView):
    @admin_required
    def post(self, request):
        data = request.data
        dataset_id = data['datasetId']
        llm_id = data['llmId']
        try:
            target = Credit.objects.get(dataset_id=dataset_id, LLM_id=llm_id)
            target.credit = None
            target.save()
        except:
            return Response({"message": "Invalid datasetId or llmId"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

class averageView(APIView):
    def get(self, request, *args, **kwargs):
        llm_id = kwargs['id']
        try:
            testing.LLMs.objects.get(id=llm_id)
        except:
            return Response({"message": "Invalid datasetId"}, status=status.HTTP_400_BAD_REQUEST)
        result = Credit.objects.filter(LLM_id=llm_id)
        average,count = 0,0
        for i in result:
            if i.credit!=None:
                average+=i.credit
                count+=1
        average/=count
        return Response({'message': 'ok', 'average': average}, status=status.HTTP_200_OK)
    
class averageListView(APIView):
    def get(self, request):
        result = testing.LLMs.objects.all()
        data=[]
        for i in result:
            average,count = 0,0
            for j in Credit.objects.filter(LLM_id=i.id):
                if j.credit!=None:
                    average+=j.credit
                    count+=1
            average/=count
            data.append(average)
        return Response({'message': 'ok', 'data': data}, status=status.HTTP_200_OK)

class commentView(APIView):
    @login_required
    def post(self, request):
        request.data['user']=request.user.id
        serializer = DatasetCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok", "id": DatasetComment.objects.last().id}, status=status.HTTP_200_OK)
        serializer = LLMCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok", "id": LLMComment.objects.last().id}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid comment"}, status=status.HTTP_400_BAD_REQUEST)
    
class datasetCommentView(APIView):
    def get(self, request, *args, **kwargs):
        dataset_id = kwargs['id']
        try:
            dataset.Dataset.objects.get(id=dataset_id)
        except:
            return Response({"message": "Invalid datasetId"}, status=status.HTTP_400_BAD_REQUEST)
        result = DatasetComment.objects.filter(dataset_id=dataset_id)
        data=[]
        for i in result:
            serializer = DatasetCommentSerializer(i)
            data.append(serializer.data)
            likes=DatasetLike.objects.filter(comment=i)
            data[-1]['like']=len(likes)
            data[-1]['add_time']=data[-1]['add_time'].split('T')[0]+' '+data[-1]['add_time'].split('T')[1][:5]
        return Response({'message': 'ok', 'data': data}, status=status.HTTP_200_OK)
    
class llmCommentView(APIView):
    def get(self, request, *args, **kwargs):
        llm_id = kwargs['id']
        try:
            testing.LLMs.objects.get(id=llm_id)
        except:
            return Response({"message": "Invalid llmId"}, status=status.HTTP_400_BAD_REQUEST)
        result = LLMComment.objects.filter(llm_id=llm_id)
        data=[]
        for i in result:
            serializer = LLMCommentSerializer(i)
            data.append(serializer.data)
            likes=LLMLike.objects.filter(comment=i)
            data[-1]['like']=len(likes)
            data[-1]['add_time']=data[-1]['add_time'].split('T')[0]+' '+data[-1]['add_time'].split('T')[1][:5]
        return Response({'message': 'ok', 'data': data}, status=status.HTTP_200_OK)
    
class likeDCommentView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            target = DatasetComment.objects.get(id=data['id'])
            try:
                like=DatasetLike.objects.get(comment=target, user=request.user)
                like.delete()
            except:
                like=DatasetLike.objects.create(comment=target, user=request.user)
                like.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid commentId"}, status=status.HTTP_400_BAD_REQUEST)

class likeLCommentView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            target = LLMComment.objects.get(id=data['id'])
            try:
                like=LLMLike.objects.get(comment=target, user=request.user)
                like.delete()
            except:
                like=LLMLike.objects.create(comment=target, user=request.user)
                like.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid commentId"}, status=status.HTTP_400_BAD_REQUEST)