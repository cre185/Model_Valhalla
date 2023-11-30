from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

'''
The ValidationErrorWithMsg is a customized exception class that inherits from APIException.
It is used to raise a 400 error with customized error message.
The error message will be placed in data['message']
'''


def get_error_details(data, default_code=None):
    if isinstance(data, list):
        ret = [
            get_error_details(item, default_code) for item in data
        ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: get_error_details(
                value,
                default_code) for key,
            value in data.items()}
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    code = getattr(data, 'code', default_code)
    return ErrorDetail(data, code)


class ValidationErrorWithMsg(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'

    def __init__(self, detail='Invalid credentials', code=None):
        if code is None:
            code = self.default_code
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = get_error_details(detail, code)
