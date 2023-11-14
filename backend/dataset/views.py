from utils.jwt import login_required
from utils.admin_required import admin_required
from .serializers import DatasetSerializer
from .models import Dataset
from testing import models as testing
from ranking import models as ranking
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

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
        return Response({"message": "ok", "datasetId": headers.data['id']}, status=status.HTTP_201_CREATED)
    
class uploadView(APIView):
    @login_required
    def post(self, request):
        target = Dataset.objects.get(id=request.data['id'])
        if not target:
            return Response({"message": "Invalid dataset id"}, status=status.HTTP_400_BAD_REQUEST)
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
        except:
            return Response({"message": "Invalid dataset id"}, status=status.HTTP_400_BAD_REQUEST)