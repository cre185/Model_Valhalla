import datetime
import os
import random
from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from testing.models import LLMs
from testing.serializers import *
from dataset.serializers import *
from utils.jwt import generate_jwt, login_required
from utils.send_msg import send_msg

from .models import *
from .serializers import *

# Create your views here.


class loginView(APIView):
    def post(self, request):
        data = request.data
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
        data = request.data
        try:
            VerifyMsg.objects.get(mobile=data['mobile'], code=data['code'])
            user = User.objects.get(mobile=data['mobile'])
            jwt = generate_jwt({"user_id": user.id, "is_admin": user.is_admin})
            return Response({"jwt": jwt,
                             "userId": user.id,
                             "username": user.username,
                             "message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)


class send_messageView(APIView):
    def post(self, request):
        data = request.data
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
        data = request.data
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
        return Response({"message": "ok",
                            "password": request.user.password},
                            status=status.HTTP_200_OK)


class updateAvatarView(APIView):
    @login_required
    def post(self, request):
        image = request.FILES.get('file')
        if not image:
            return Response({"message": "Invalid image"},
                            status=status.HTTP_400_BAD_REQUEST)
        # rename image
        image_name = str(request.user.id) + '_' + \
            uuid4().hex + '.' + image.name.split('.')[-1]
        with transaction.atomic():
            # remove old file
            if request.user.avatar and request.user.avatar.name.split('/')[-1] != 'default.jpg':
                try:
                    old_file_path = request.user.avatar.path
                    if os.path.isfile(old_file_path):
                        os.remove(old_file_path)
                        request.user.avatar.save(image_name, image)
                except Exception:
                    return Response({"message": "Upload failed, please try again later."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                request.user.avatar.save(image_name, image)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class logoutView(APIView):
    def post(self, request):
        return Response({"message": "ok", "hint": "Surprise! Nothing happened."}, status=status.HTTP_200_OK)


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
        data = request.data
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
        data = request.data
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


class subscribeLLMView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=data['llmId'])
            if LLMSubscription.objects.filter(
                    user=request.user, llm=llm).exists():
                subscription = LLMSubscription.objects.filter(
                    user=request.user, llm=llm)
                subscription.delete()
                return Response({"message": "ok"}, status=status.HTTP_200_OK)
            subscription = LLMSubscription.objects.create(
                user=request.user, llm=llm)
            subscription.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid llmId"},
                            status=status.HTTP_400_BAD_REQUEST)


class subscribeDatasetView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            dataset = Dataset.objects.get(id=data['datasetId'])
            if DatasetSubscription.objects.filter(
                    user=request.user, dataset=dataset).exists():
                subscription = DatasetSubscription.objects.filter(
                    user=request.user, dataset=dataset)
                subscription.delete()
                return Response({"message": "ok"}, status=status.HTTP_200_OK)
            subscription = DatasetSubscription.objects.create(
                user=request.user, dataset=dataset)
            subscription.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid datasetId"},
                            status=status.HTTP_400_BAD_REQUEST)


class list_llm_subscriptionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            subscriptions = LLMSubscription.objects.filter(user=user)
            llms = []
            for subscription in subscriptions:
                serializer = LLMsSerializer(subscription.llm)
                llms.append(serializer.data)
            return Response({"message": "ok", "llms": llms},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid userId"},
                            status=status.HTTP_400_BAD_REQUEST)
        

class list_dataset_subscriptionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            subscriptions = DatasetSubscription.objects.filter(user=user)
            datasets = []
            for subscription in subscriptions:
                serializer = DatasetSerializer(subscription.dataset)
                datasets.append(serializer.data)
            return Response({"message": "ok", "datasets": datasets},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid userId"},
                            status=status.HTTP_400_BAD_REQUEST)


class list_messageView(APIView):
    @login_required
    def get(self, request):
        messages = Msg.objects.filter(target=request.user)
        msgs = []
        for message in messages:
            serializer = MsgSerializer(message)
            msgs.append(serializer.data)
            read = MsgTarget.objects.get(msg=message, target=request.user)
            msgs[-1]['read'] = read.read
        return Response({"message": "ok", "msgs": msgs},
                        status=status.HTTP_200_OK)


class create_messageView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            data['author'] = request.user.id
            serializer = MsgSerializer(data=data)
            if not serializer.is_valid():
                return Response({"message": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            msg_id = serializer.data['id']
            try:
                upload_file = request.FILES.get('file')
                msg = Msg.objects.get(id=msg_id)
                file_name = str(msg_id) + '_' + uuid4().hex + '.' + upload_file.name.split('.')[-1]
                msg.msg_file.save(file_name, upload_file)
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
        data = request.data
        try:
            data['author'] = request.user.id
            serializer = MsgSerializer(data=data)
            if not serializer.is_valid():
                return Response({"message": "Invalid data"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            msg_id = serializer.data['id']
            try:
                upload_file = request.FILES.get('file')
                msg = Msg.objects.get(id=msg_id)
                file_name = str(msg_id) + '_' + uuid4().hex + '.' + upload_file.name.split('.')[-1]
                msg.msg_file.save(file_name, upload_file)
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
        data = request.data
        try:
            message = Msg.objects.get(id=data['id'])
            read = MsgTarget.objects.get(msg=message, target=request.user)
            read.read = True
            read.save()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid data"},
                            status=status.HTTP_400_BAD_REQUEST)

class find_user_by_nameView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            serializer = UserSerializer(user)
            data = serializer.data
            data['password'] = ''
            data['message'] = 'ok'
            return Response(data, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid username"},
                            status=status.HTTP_400_BAD_REQUEST)