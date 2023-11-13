import os
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class send_msg():
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send_sms(
        code, mobile
    ) -> None:
        client = send_msg.create_client('LTAI5tHGsxM3XG7zoCaJHH7K', '9tl5euDkZcI727MF5gUw92IXIhiBIW')
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=mobile,
            sign_name='模型竞技场',
            template_code='SMS_463715951',
            template_param='{\"code\":' + str(code) + '}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            print(client.send_sms_with_options(send_sms_request, runtime))
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
