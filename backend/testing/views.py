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
    