import json
from django.shortcuts import render
from .serializers import DatasetSerializer
from .models import Dataset
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
        data = JSONParser().parse(request)
        serializer = DatasetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
