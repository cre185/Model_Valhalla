import json
from django.shortcuts import render
from .serializers import DatasetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
# Create your views here.

@api_view(["POST"])
def upload(request):
    try:
        data = JSONParser().parse(request)
        serializer = DatasetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({"message": "Bad arguments"}, status=status.HTTP_400_BAD_REQUEST)