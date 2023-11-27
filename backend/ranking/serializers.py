from rest_framework import serializers

from .models import *


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'

    def validate_credit(self, credit):
        if credit is not None:
            if credit < 0:
                raise serializers.ValidationError("Credit should be a positive number.")
            if credit > 100:
                raise serializers.ValidationError("Credit should be less than 100.")
        return credit

class DatasetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetComment
        fields = '__all__'

    def validate_comment(self, comment):
        if len(comment) > 1000:
            raise serializers.ValidationError("Comment should be less than 1000 characters.")
        elif len(comment) == 0:
            raise serializers.ValidationError("Comment should not be empty.")
        return comment
    
class LLMCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMComment
        fields = '__all__'

    def validate_comment(self, comment):
        if len(comment) > 1000:
            raise serializers.ValidationError("Comment should be less than 1000 characters.")
        elif len(comment) == 0:
            raise serializers.ValidationError("Comment should not be empty.")
        return comment