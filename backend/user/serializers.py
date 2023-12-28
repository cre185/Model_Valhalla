import datetime
import re

from rest_framework import serializers

from utils.validation_error import ValidationErrorWithMsg

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, username):
        # if username already exists
        if User.objects.filter(username=username).count():
            if self.context['request'].method == 'PATCH' and str(self.context['request'].path).split(
                    '/')[-1] == str(User.objects.get(username=username).id):
                return username
            raise ValidationErrorWithMsg(
                detail={'message': 'Username already been used'})
        # if username is valid
        if re.match(r'^[a-zA-Z0-9_-]{6,32}$', username) is None:
            raise ValidationErrorWithMsg(
                detail={'message': 'Username is invalid'})

        return username

    def validate_password(self, password):
        # if password is valid
        if re.match(r'^[a-zA-Z0-9_-]{6,32}$', password) is None:
            raise ValidationErrorWithMsg(
                detail={'message': 'Password is invalid'})

        return password

    def validate_mobile(self, mobile):
        # if mobile already exists
        if User.objects.filter(mobile=mobile).count():
            if self.context['request'].method == 'PATCH' and str(self.context['request'].path).split(
                    '/')[-1] == str(User.objects.get(mobile=mobile).id):
                return mobile
            raise ValidationErrorWithMsg(
                detail={'message': 'Mobile already been used'})
        # if mobile is valid
        if re.match(r'^\d{11}$', mobile) is None:
            raise ValidationErrorWithMsg(
                detail={'message': 'Mobile is invalid'})

        return mobile

    def validate_email(self, email):
        # if email already exists
        if User.objects.filter(email=email).count():
            if self.context['request'].method == 'PATCH' and str(
                    self.context['request'].path).split('/')[-1] == str(User.objects.get(email=email).id):
                return email
            raise ValidationErrorWithMsg(
                detail={'message': 'Email already been used'})
        # if email is valid
        if re.match(
            r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',
                email) is None:
            raise ValidationErrorWithMsg(
                detail={'message': 'Email is invalid'})

        return email


class VerifyMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyMsg
        fields = '__all__'

    def validate_mobile(self, mobile):
        # if mobile is valid
        if re.match(r'^\d{11}$', mobile) is None:
            raise ValidationErrorWithMsg(
                detail={'message': 'Mobile is invalid'})
        # if code has been sent in one minute
        one_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0,
                                                                      minutes=1, seconds=0)
        if VerifyMsg.objects.filter(
                add_time__gt=one_minute_age,
                mobile=mobile).count():
            raise ValidationErrorWithMsg(
                detail={'message': 'Code has been sent in one minute'})
        # remove former codes
        history_records = VerifyMsg.objects.filter(
            add_time__lt=one_minute_age, mobile=mobile)
        if history_records:
            history_records.delete()

        return mobile


class VerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyEmail
        fields = '__all__'

    def validate_email(self, email):
        # if email is valid
        if re.match(
            r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',
                email) is None:
            raise ValidationErrorWithMsg(
                detail={'message': 'Email is invalid'})
        # if code has been sent in one minute
        one_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0,
                                                                      minutes=1, seconds=0)
        if VerifyEmail.objects.filter(
                add_time__gt=one_minute_age,
                email=email).count():
            raise ValidationErrorWithMsg(
                detail={'message': 'Code has been sent in one minute'})
        # remove former codes
        history_records = VerifyEmail.objects.filter(
            add_time__lt=one_minute_age, email=email)
        if history_records:
            history_records.delete()

        return email


class MsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Msg
        fields = '__all__'
