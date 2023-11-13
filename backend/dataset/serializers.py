from rest_framework import serializers
from .models import Dataset
from utils.validation_error import ValidationErrorWithMsg

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

    def validate_name(self, name):
        # if the name has already been used
        if Dataset.objects.filter(name=name).exists():
            raise ValidationErrorWithMsg('The name has already been used.')
        return name