
import base64
import datetime

import jwt
import pytz
import scrypt
from django.conf import settings
from django.http import JsonResponse

from user.models import User


def generate_jwt(payload, expiry=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :return: 生成jwt
    """
    if expiry is None:
        now = datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))
        expire_hours = (
            int(settings.JWT_EXPIRE_HOURS)
            if int(settings.JWT_EXPIRE_HOURS) > 0
            else 1
        )
        expiry = now + datetime.timedelta(hours=expire_hours)
        # print("now:", now)
        # print("expiry:", expiry)

    _payload = {"exp": expiry}
    _payload.update(payload)

    secret = settings.JWT_SECRET

    token = jwt.encode(_payload, secret, algorithm="HS256")

    return token


def verify_jwt(token):
    """
    校验jwt
    :param token: jwt
    :return: dict: payload
    """
    secret = settings.JWT_SECRET

    try:
        if token.startswith("Bearer "):
            token = token[7:]
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        payload = None

    return payload


def encrypt_password(password):
    salt = settings.SALT
    key = scrypt.hash(password, salt, 32768, 8, 1, 32)
    return base64.b64encode(key).decode("ascii")


def jwt_authentication(request):
    """
    根据jwt验证用户身份
    """
    request.user = None
    token = request.headers.get("Authorization")
    if token:
        payload = verify_jwt(token)
        if payload:
            user_id = payload.get("user_id")
            try:
                user = User.objects.get(id=user_id)
                request.user = user
                return 1
            except User.DoesNotExist:
                pass
        else:
            return 2
    return 0


def login_required(func):
    # @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        res = jwt_authentication(request)
        if res == 0:
            return JsonResponse(
                {"message": "User must be authorized."}, status=401
            )
        elif res == 2:
            return JsonResponse(
                {"message": "Token has expired."}, status=401
            )
        else:
            response = func(self, request, *args, **kwargs)
            jwt = generate_jwt({"user_id": request.user.id, "is_admin": request.user.is_admin})
            response.data['jwt'] = jwt
            return response

    return wrapper
