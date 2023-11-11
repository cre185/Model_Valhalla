from rest_framework import serializers
from .models import LLMs
from utils.validation_error import ValidationErrorWithMsg

class LLMsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMs
        fields = ('id', 'name', 'add_time')

    def validate_name(self, name):
        # if the name has already been used
        if LLMs.objects.filter(name=name).exists():
            raise ValidationErrorWithMsg('The name has already been used.')
        return name