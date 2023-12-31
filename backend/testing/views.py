import os
from uuid import uuid4

from django.db import transaction
from django.http import StreamingHttpResponse
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dataset.models import *
from ranking.models import *
from utils.admin_required import admin_required
from utils.auto_test import *
from utils.elo_rating import *
from utils.jwt import login_required

from .models import *
from .serializers import *

# Create your views here.


class createView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer

    @login_required
    def post(self, request):
        headers = self.create(request)
        llm = LLMs.objects.get(id=headers.data['id'])
        for data in dataset.Dataset.objects.all():
            Credit.objects.create(LLM=llm, dataset=data, credit=None)
        return Response({"message": "ok",
                         "llmId": headers.data['id']},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class deleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer

    @admin_required
    def delete(self, request, *args, **kwargs):
        try:
            instance = LLMs.objects.get(id=int(kwargs['id']))
            instance.delete()
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid llm id"},
                            status=status.HTTP_400_BAD_REQUEST)


class updateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer
    lookup_field = "id"

    @admin_required
    def patch(self, request, *args, **kwargs):
        result = self.partial_update(request, *args, **kwargs)
        data = result.data
        data['message'] = 'ok'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)


class retrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        result = self.retrieve(request, *args, **kwargs)
        data = result.data
        data['message'] = 'ok'
        data['add_time'] = data['add_time'].split('T')[0]
        return Response(data, status=status.HTTP_200_OK)


class listView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = LLMs.objects.all()
    serializer_class = LLMsSerializer

    def get(self, request, *args, **kwargs):
        result = self.list(request, *args, **kwargs)
        data = result.data
        for i in range(len(data)):
            data[i]['add_time'] = data[i]['add_time'].split('T')[0]
        return Response({'message': 'ok', 'data': data},
                        status=status.HTTP_200_OK)


class uploadView(APIView):
    @login_required
    def post(self, request):
        try:
            llm = LLMs.objects.get(id=int(request.data['llmId']))
        except BaseException:
            return Response({"message": "Invalid llm id"},
                            status=status.HTTP_400_BAD_REQUEST)
        logo = request.FILES.get('file')
        if not logo:
            return Response({"message": "Invalid logo"},
                            status=status.HTTP_400_BAD_REQUEST)
        # rename file
        logo_name = str(llm.id) + '_' + uuid4().hex + \
            '.' + logo.name.split('.')[-1]
        with transaction.atomic():
            # remove old file
            if llm.logo:
                try:
                    old_file_path = llm.logo.path
                    if os.path.isfile(old_file_path):
                        os.remove(old_file_path)
                        llm.logo.save(logo_name, logo)
                except Exception:
                    return Response({"message": "Upload failed, please try again later."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                llm.logo.save(logo_name, logo)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class testView(APIView):
    # todo: change it to non-blocking
    @login_required
    def post(self, request):
        data = request.data
        obj_dataset = Dataset.objects.filter(subjective=False)
        target = Credit.objects.filter(dataset__in=obj_dataset)
        if 'llmId' in data:
            target = target.filter(LLM_id=int(data['llmId']))
        if 'datasetId' in data:
            target = target.filter(dataset_id=int(data['datasetId']))
        if 'style' in data and data['style'] == 'fill':
            target = target.filter(credit__isnull=True)

        if target.count() == 0:
            return Response(
                {"message": "No tests are carried out"}, status=status.HTTP_200_OK)
        for tar in target:
            dataset = tar.dataset
            llm = tar.LLM
            if not dataset.data_file:
                continue
            if not llm.api_url:
                continue
            autoTest = AutoTest(llm)
            result = autoTest.whole_test(dataset.data_file.path)
            correct_amount = result[0]
            amount = result[1]
            tar.credit_list.append((100.0 * correct_amount) / amount)
            tar.credit = sum(tar.credit_list) / len(tar.credit_list)
            tar.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class battleMatchView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=int(data['llmId']))
            all_others = LLMs.objects.exclude(id=llm.id)
            if all_others.count() == 0:
                return Response({"message": "No other llms"},
                                status=status.HTTP_200_OK)
            nearest = all_others[0]
            for other in all_others:
                if abs(
                        other.elo_credit -
                        llm.elo_credit) < abs(
                        nearest.elo_credit -
                        llm.elo_credit):
                    nearest = other
            return Response({"message": "ok", "llmId": nearest.id},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid parameters"},
                            status=status.HTTP_400_BAD_REQUEST)


class battleResultView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = BattleHistory.objects.all()
    serializer_class = BattleHistorySerializer

    @login_required
    def post(self, request):
        try:
            data = request.data
            data['user_id'] = request.user.id
            llm1 = LLMs.objects.get(id=int(data['llm1']))
            llm2 = LLMs.objects.get(id=int(data['llm2']))
            if llm1.id == llm2.id:
                return Response({"message": "Invalid parameters"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            sa = (int(data['winner']) + 1.0) / 2
            elo = EloRating()
            llm1.elo_credit, llm2.elo_credit = elo.cal_result(
                llm1.elo_credit, llm2.elo_credit, sa)
            llm1.save()
            llm2.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers)
        except BaseException:
            return Response({"message": "Invalid parameters"},
                            status=status.HTTP_400_BAD_REQUEST)


class battleHistoryView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            llm = LLMs.objects.get(id=int(data['llm']))
            history = BattleHistory.objects.filter(
                llm1=llm) | BattleHistory.objects.filter(
                llm2=llm)
            return Response({"message": "ok", "data": BattleHistorySerializer(
                history, many=True).data}, status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid parameters"},
                            status=status.HTTP_400_BAD_REQUEST)


class generateView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=int(data['llmId']))
            autotest = AutoTest(llm)
            ans = autotest.call_api(data['prompt'])
            return Response({"message": "ok", "content": ans},
                            status=status.HTTP_200_OK)
        except BaseException:
            return Response({"message": "Invalid parameters"},
                            status=status.HTTP_400_BAD_REQUEST)


class streamGenerateView(APIView):
    @login_required
    def post(self, request):
        data = request.data
        try:
            llm = LLMs.objects.get(id=int(data['llmId']))
            autotest = AutoTest(llm)
            response_generator = autotest.stream_call_api(data['prompt'])
            return StreamingHttpResponse(
                response_generator, content_type="text/plain")
        except BaseException:
            return Response({"message": "Invalid parameters"},
                            status=status.HTTP_400_BAD_REQUEST)
