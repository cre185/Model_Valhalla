import datetime
import random
from .models import User, VerifyMsg, VerifyEmail
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyMsgSerializer, VerifyEmailSerializer, VerifyResetSerializer
from utils.jwt import generate_jwt, login_required
from utils.send_msg import send_msg
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
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
        jwt = generate_jwt({"user_id": user.id, "is_admin": user.is_admin})
        return Response({"jwt": jwt, 
                        "userId": user.id,
                        "username": user.username,
                        "message": "ok"}, status=status.HTTP_200_OK)
    
class login_with_verify_codeView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_msg = VerifyMsg.objects.get(mobile=data['mobile'], code=data['code'])
            try:
                user = User.objects.get(mobile=data['mobile'])
            except:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            jwt = generate_jwt({"user_id": user.id, "is_admin": user.is_admin})
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

class verify_codeView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_msg = VerifyMsg.objects.get(mobile=data['mobile'], code=data['code'])
            add_time = verify_msg.add_time
            due_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
            if add_time <= due_time:
                return Response({'message':'Code expired'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)

class registerView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        headers = self.create(request)
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED, headers=headers)
    
class updateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    @login_required
    def put(self, request, *args, **kwargs):
        result = self.update(request, *args, **kwargs)
        if request.user.id != int(kwargs['id']):
            return Response({"message": "User must be authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        data = result.data
        data['message'] = 'ok'
        data['password'] = '********'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)
    
    @login_required
    def patch(self, request, *args, **kwargs):
        result = self.partial_update(request, *args, **kwargs)
        if request.user.id != int(kwargs['id']):
            return Response({"message": "User must be authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        data = result.data
        data['message'] = 'ok'
        data['password'] = '********'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)
    
class retrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    
    @login_required
    def get(self, request, *args, **kwargs):
        result = self.retrieve(request, *args, **kwargs)
        if request.user.id != int(kwargs['id']):
            return Response({"message": "User must be authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        data = result.data
        data['message'] = 'ok'
        data['password'] = '********'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)
    
class updateAvatarView(APIView):
    @login_required
    def post(self, request):
        dict = request.FILES
        image = dict['file']
        request.user.avatar = image
        request.user.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

class logoutView(APIView):
    @login_required
    def post(self, request):
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
    
class deleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    
    @login_required
    def delete(self, request, *args, **kwargs):
        if request.user.id != int(kwargs['id']) and not request.user.is_admin:
            return Response({"message": "User must be authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        result = self.destroy(request, *args, **kwargs)
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
            add_time = verify_email.add_time
            due_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
            if add_time <= due_time:
                return Response({'message': 'Code expired'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)

class send_resetEmailView(APIView):
    @login_required
    def post(self, request):
        user_email = request.user.email
        data = JSONParser().parse(request)
        data["code"] = random.randint(100000, 999999)
        data["email"] = user_email
        serializer = VerifyResetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            send_mail(
                subject="Model_Valhalla 重置密码验证码",
                message=("您的验证码为：" + str(data["code"]) + "，请于十分钟内填写"),
                from_email=settings.EMAIL_FROM,
                recipient_list=[data["email"]],
                fail_silently=False
            )
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class reset_passwordView(APIView):
    @login_required
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_email = ResetPassword.objects.get(email=data['email'], code=data['code'])
            add_time = verify_email.add_time
            due_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
            if add_time <= due_time:
                return Response({'message':'Code expired'}, status=status.HTTP_400_BAD_REQUEST)
            now_user = User.objects.get(email=data['email'])
            now_user.password = data['new_password']
            # verify_email.delete()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)
