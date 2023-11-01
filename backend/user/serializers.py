import datetime
from rest_framework import serializers
from .models import User, VerifyMsg

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'add_time')

class VerifyMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyMsg
        fields = ('mobile', 'code', 'add_time')

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('手机号码已经注册')

        # 验证手机号码合法

        # 验证码发送频率
        one_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        if VerifyMsg.objects.filter(add_time__gt=one_minute_age, mobile=mobile).count():
            raise serializers.ValidationError('请一分钟后再次发送')

        return mobile