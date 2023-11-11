from .serializers import DatasetSerializer
from .models import Dataset
from testing import models as testing
from ranking import models as ranking
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# Create your views here.

class uploadView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    def post(self, request):
        headers = self.create(request)
        data = Dataset.objects.get(id=headers.data['id'])
        for llm in testing.LLMs.objects.all():
            ranking.Credit.objects.create(LLM=llm, dataset=data, credit=None)
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)
