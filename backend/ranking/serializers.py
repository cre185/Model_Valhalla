from .models import Credit
from rest_framework import serializers

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
