import datetime
import random

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, mixins, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from testing.models import LLMs
from testing.serializers import *
from utils.jwt import generate_jwt, login_required
from utils.send_msg import send_msg

from .models import *
from .serializers import *

# Create your views here.


class loginView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            user = User.objects.get(
                username=data['username'],
                password=data['password'])
        except BaseException:
            return Response({"message": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)
        jwt = generate_jwt({"user_id": user.id, "is_admin": user.is_admin})
        return Response({"jwt": jwt,
                        "userId": user.id,
                         "username": user.username,
                         "message": "ok"}, status=status.HTTP_200_OK)


class login_with_verify_codeView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_msg = VerifyMsg.objects.get(
                mobile=data['mobile'], code=data['code'])
            try:
                user = User.objects.get(mobile=data['mobile'])
            except BaseException:
                return Response({"message": "Invalid credentials"},
                                status=status.HTTP_401_UNAUTHORIZED)
            jwt = generate_jwt({"user_id": user.id, "is_admin": user.is_admin})
            return Response({"jwt": jwt,
                            "userId": user.id,
                             "username": user.username,
                             "message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid code"},
                            status=status.HTTP_401_UNAUTHORIZED)


class send_messageView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        data["code"] = random.randint(100000, 999999)
        serializer = VerifyMsgSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            send = send_msg()
            send.send_sms(data["code"], data["mobile"])
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class verify_codeView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            verify_msg = VerifyMsg.objects.get(
                mobile=data['mobile'], code=data['code'])
            add_time = verify_msg.add_time
            due_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
            if add_time <= due_time:
                return Response({'message': 'Code expired'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid code"},
                            status=status.HTTP_401_UNAUTHORIZED)


class registerView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        request.data['is_admin'] = False
        if 'secret' in request.data and request.data['secret'] == 'TXNKvJ#1':
            request.data['is_admin'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


class updateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    @login_required
    def put(self, request, *args, **kwargs):
        result = self.update(request, *args, **kwargs)
        if request.user.id != int(kwargs['id']):
            return Response({"message": "User must be authorized."},
                            status=status.HTTP_401_UNAUTHORIZED)
        data = result.data
        data['message'] = 'ok'
        return Response(data, status=status.HTTP_200_OK)

    @login_required
    def patch(self, request, *args, **kwargs):
        result = self.partial_update(request, *args, **kwargs)
        if request.user.id != int(kwargs['id']):
            return Response({"message": "User must be authorized."},
                            status=status.HTTP_401_UNAUTHORIZED)
        data = result.data
        data['message'] = 'ok'
        return Response(data, status=status.HTTP_200_OK)


class retrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        result = self.retrieve(request, *args, **kwargs)
        if kwargs["id"] != int(kwargs['id']):
            return Response({"message": "User must be authorized."},
                            status=status.HTTP_401_UNAUTHORIZED)
        data = result.data
        data['message'] = 'ok'
        data['password'] = '**********'
        return Response(data, status=status.HTTP_200_OK)


class retrievePasswordView(APIView):
    @login_required
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            return Response({"message": "ok",
                             "password": user.password},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)


class updateAvatarView(APIView):
    @login_required
    def post(self, request):
        dict = request.FILES
        image = dict['file']
        if request.user.avatar.name == 'static/avatar/default.jpg':
            request.user.avatar = image
            request.user.save()
        else:
            request.user.avatar.delete(save=False)
            request.user.avatar.save(image.name, image)
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
            return Response({"message": "User must be authorized."},
                            status=status.HTTP_401_UNAUTHORIZED)
        self.destroy(request, *args, **kwargs)
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
                message=("您的验证码为：" + str(data["code"]) + "，如果不是本人操作，请忽略此消息。"),
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
            verify_email = VerifyEmail.objects.get(
                email=data['email'], code=data['code'])
            add_time = verify_email.add_time
            due_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
            if add_time <= due_time:
                return Response({'message': 'Code expired'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid code"},
                            status=status.HTTP_401_UNAUTHORIZED)


class subscribeView(APIView):
    @login_required
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            llm = LLMs.objects.get(id=data['llmId'])
            if Subscription.objects.filter(
                    user=request.user, llm=llm).exists():
                subscription = Subscription.objects.get(
                    user=request.user, llm=llm)
                subscription.delete()
                return Response({"message": "ok"}, status=status.HTTP_200_OK)
            subscription = Subscription.objects.create(
                user=request.user, llm=llm)
            subscription.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid llmId"},
                            status=status.HTTP_400_BAD_REQUEST)


class list_subscriptionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            subscriptions = Subscription.objects.filter(user=user)
            llms = []
            for subscription in subscriptions:
                serializer = LLMsSerializer(subscription.llm)
                llms.append(serializer.data)
            return Response({"message": "ok", "llms": llms},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid userId"},
                            status=status.HTTP_400_BAD_REQUEST)


class list_messageView(APIView):
    @login_required
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            messages = Msg.objects.filter(target=user)
            msgs = []
            for message in messages:
                serializer = MsgSerializer(message)
                msgs.append(serializer.data)
                read = MsgTarget.objects.get(msg=message, target=user)
                msgs[-1]['read'] = read.read
            return Response({"message": "ok", "msgs": msgs},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid userId"},
                            status=status.HTTP_400_BAD_REQUEST)


class create_messageView(APIView):
    @login_required
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            data['author'] = request.user.id
            serializer = MsgSerializer(data=data)
            if not serializer.is_valid():
                return Response({"message": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            msg_id = serializer.data['id']
            try:
                upload_file = request.FILES['file']
                msg = Msg.objects.get(id=msg_id)
                msg.msg_file = upload_file
                msg.save()
            except BaseException:
                pass
            for target in data['target']:
                msg_target = MsgTarget.objects.create(
                    msg_id=msg_id, target_id=target)
                msg_target.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        except BaseException:
            return Response({"message": "Invalid data"},
                            status=status.HTTP_400_BAD_REQUEST)


class create_message_to_adminView(APIView):
    @login_required
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            data['author'] = request.user.id
            serializer = MsgSerializer(data=data)
            if not serializer.is_valid():
                return Response({"message": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            msg_id = serializer.data['id']
            try:
                upload_file = request.FILES['file']
                msg = Msg.objects.get(id=msg_id)
                msg.msg_file = upload_file
                msg.save()
            except BaseException:
                pass
            admin = User.objects.filter(is_admin=True)
            for target in admin:
                msg_target = MsgTarget.objects.create(
                    msg_id=msg_id, target_id=target.id)
                msg_target.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        except BaseException:
            return Response({"message": "Invalid data"},
                            status=status.HTTP_400_BAD_REQUEST)


class check_messageView(APIView):
    @login_required
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            message = Msg.objects.get(id=data['id'])
            read = MsgTarget.objects.get(msg=message, target=request.user)
            read.read = True
            read.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid data"},
                            status=status.HTTP_400_BAD_REQUEST)
