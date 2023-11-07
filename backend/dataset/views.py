import json
from django.shortcuts import render
from .serializers import DatasetSerializer
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class uploadView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = DatasetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
