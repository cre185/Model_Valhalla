from backend.utils.jwt import login_required
from backend.utils.admin_required import admin_required
from .serializers import CreditSerializer
from .models import Credit
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# Create your views here.

class updateView(APIView):
    @admin_required
    def post(self, request):
        data = request.data
        dataset_id = data['datasetId']
        llm_id = data['llmId']
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