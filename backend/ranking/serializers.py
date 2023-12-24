from rest_framework import serializers

from utils.validation_error import ValidationErrorWithMsg

from .models import *


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'


class DatasetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetComment
        fields = '__all__'

    def validate_comment(self, comment):
        if len(comment) > 1000:
            raise ValidationErrorWithMsg(
                "Comment should be less than 1000 characters.")
        elif len(comment) == 0:
            raise ValidationErrorWithMsg("Comment should not be empty.")
        return comment


class LLMCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMComment
        fields = '__all__'

    def validate_comment(self, comment):
        if len(comment) > 1000:
            raise ValidationErrorWithMsg(
                "Comment should be less than 1000 characters.")
        elif len(comment) == 0:
            raise ValidationErrorWithMsg("Comment should not be empty.")
        return comment
