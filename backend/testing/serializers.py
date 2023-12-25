import json

from rest_framework import serializers

from user.models import *
from utils.validation_error import ValidationErrorWithMsg

from .models import *


class LLMsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMs
        fields = '__all__'

    def validate_name(self, name):
        # if the name has already been used
        if LLMs.objects.filter(name=name).exists():
            if self.context['request'].method == 'PATCH' and str(self.context['request'].path).split('/')[-1] == str(LLMs.objects.get(name=name).id):
                return name
            raise ValidationErrorWithMsg('The name has already been used.')
        return name

    def validate_api_RPM(self, api_RPM):
        if api_RPM < 1:
            raise ValidationErrorWithMsg('Invalid RPM value.')
        return api_RPM


class BattleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleHistory
        fields = '__all__'

    def validate_user_id(self, user_id):
        if not User.objects.filter(id=user_id).exists():
            raise ValidationErrorWithMsg('User does not exist.')
        return user_id

    def validate_winner(self, winner):
        if winner != 1 and winner != 0 and winner != -1:
            raise ValidationErrorWithMsg('Invalid winner value.')
        return winner
