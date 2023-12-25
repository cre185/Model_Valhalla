from rest_framework import serializers

from utils.validation_error import ValidationErrorWithMsg

from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

    def validate_name(self, name):
        # if the name has already been used
        if Dataset.objects.filter(name=name).exists():
            if self.context['request'].method == 'PATCH' and str(self.context['request'].path).split('/')[-1] == str(Dataset.objects.get(name=name).id):
                return name
            raise ValidationErrorWithMsg('The name has already been used.')
        return name
