from rest_framework import serializers
from .models import Dataset
from utils.validation_error import ValidationErrorWithMsg

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'add_time')

    def validate_name(self, name):
        # maybe there will be validation requirements...
        return name