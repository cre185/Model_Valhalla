import json
import random
from django.http import HttpResponse, JsonResponse
from .models import User, VerifyMsg
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyMsgSerializer
from utils.jwt import encrypt_password, generate_jwt, login_required
from utils.send_msg import send_msg

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the user index.")

@api_view(["POST", "OPTIONS"])
def login(request):
    if request.method == "OPTIONS":
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    try:
        data = JSONParser().parse(request)
        try:
            user = User.objects.get(username=data['username'], password=data['password'])
        except:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        jwt = generate_jwt({"user_id": user.id, "username": user.username})
        return Response({"jwt": jwt, 
                                "userId": user.id,
                                "username": user.username,
                                "message": "ok"}, status=status.HTTP_200_OK)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Bad arguments"}, status=400)

@api_view(["POST"])
def send_message(request):  
    data = JSONParser().parse(request)
    data["code"] = random.randint(100000, 999999)
    serializer = VerifyMsgSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        # send_msg.send_sms(serializer.code, serializer.mobile)
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@login_required
def logout(request):
    return JsonResponse({"message": "ok"})