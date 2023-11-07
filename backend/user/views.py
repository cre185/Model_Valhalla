import json
import random
import re
import time
from django.http import HttpResponse, JsonResponse
from .models import User, VerifyMsg
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyMsgSerializer
from utils.jwt import encrypt_password, generate_jwt, login_required
from utils.send_msg import send_msg

# Create your views here.

@api_view(["POST", "OPTIONS"])
def login(request):
    if request.method == "OPTIONS":
        return Response({"message": "ok"}, status=status.HTTP_204_NO_CONTENT)
    
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
        return Response({"message": "Bad arguments"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def login_with_verify_code(request):
    data = JSONParser().parse(request)
    try:
        verify_msg = VerifyMsg.objects.get(mobile=data['mobile'], code=data['code'])
        try:
            user = User.objects.get(mobile=data['mobile'])
        except:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        jwt = generate_jwt({"user_id": user.id, "username": user.username})
        return Response({"jwt": jwt, 
                        "userId": user.id,
                        "username": user.username,
                        "message": "ok"}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def send_message(request):  
    data = JSONParser().parse(request)
    data["code"] = random.randint(100000, 999999)
    serializer = VerifyMsgSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        send = send_msg()
        # send.send_sms(data["code"], data["mobile"])
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def verify_code(request):
    data = JSONParser().parse(request)
    try:
        verify_msg = VerifyMsg.objects.get(mobile=data['mobile'], code=data['code'])
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST", "OPTION"])
def register(request):
    if request.method == "OPTIONS":
        return Response({"message": "ok"}, status=status.HTTP_204_NO_CONTENT)

    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def logout(request):
    return JsonResponse({"message": "ok"})

'''def generate_email_verifycode():  # 生成6位的验证码
    codes = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    random.seed(int(time.time()))
    for i in range(6):
        res += codes[random.randint(0, len(codes)-1)]
    return res'''

'''def send_email_verifycode():
    if req.method == "GET":
        body = req.GET
        username = body.get('username')
        user = User.objects.filter(name=username).first()

        if not user:
            return Response({"message": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

        if user.email_address == "":
            return Response({"message": "用户未绑定邮箱"}, status=status.HTTP_400_BAD_REQUEST)

        if (time.time() - user.email_verifycode_time) >= 300:
            return Response({"message": "您已经在5分钟内获得过验证码，请稍后重试"}, status=status.HTTP_400_BAD_REQUEST)

        # 如果需要的话可以再给user加一个时间属性，判断验证码是否过期
        verify_code = generate_email_verifycode()
        user.email_verifycode = verify_code
        user.email_verifycode_time = time.time()
        user.save()

        send_mail(
            subject="Mode_Valhalla 用户密码找回",
            message=("您的验证码为：" + verify_code),
            from_email="",  # 这一块需要固定设置一个发送邮箱，可以后续商量
            recipient_list=[user.email_address],
            fail_silently=False
        )
        return Response({"message": "验证码已发送"}, status=status.HTTP_200_OK)

    return Response({"message": "Bad Method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)'''
