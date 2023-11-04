import requests
import json

# not working now...
class send_msg(object):

    def __init__(self):
        self.api_key = '898d5b2d092de1ba2e01beb7a4a0498c'
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '您的验证码是'+str(code)+'。如非本人操作，请忽略本短信。',
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict