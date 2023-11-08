import random
from .models import User, VerifyMsg, VerifyEmail
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyMsgSerializer, VerifyEmailSerializer
from utils.jwt import encrypt_password, generate_jwt, login_required
from utils.send_msg import send_msg
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# Create your views here.

class loginView(APIView):
    def post(self, request):
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
    
    def options(self, request):
        return Response({"message": "ok"}, status=status.HTTP_204_NO_CONTENT)
    
class login_with_verify_codeView(APIView):
    def post(self, request):
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

class send_messageView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        data["code"] = random.randint(100000, 999999)
        serializer = VerifyMsgSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            send = send_msg()
            # send.send_sms(data["code"], data["mobile"])
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def options(self, request):
        return Response({"message": "ok"}, status=status.HTTP_204_NO_CONTENT)

class verify_codeView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_msg = VerifyMsg.objects.get(mobile=data['mobile'], code=data['code'])
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)

class registerView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        headers = self.create(request)
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)
    
    def options(self, request):
        return Response({"message": "ok"}, status=status.HTTP_204_NO_CONTENT)

class logoutView(APIView):
    @login_required
    def post(self, request):
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    
class send_emailView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        data["code"] = random.randint(100000, 999999)
        serializer = VerifyEmailSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            send_mail(
                subject="Model_Valhalla 验证码",
                message=("您的验证码为：" + str(data["code"])),
                from_email=settings.EMAIL_FROM,
                recipient_list=[data["email"]],
                fail_silently=False
            )
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class verify_emailView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_email = VerifyEmail.objects.get(email=data['email'], code=data['code'])
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)