from .jwt import *


def admin_required(func):
    # @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        res = jwt_authentication(request)
        if res == 0 or request.user is None:
            return JsonResponse(
                {"message": "User must be authorized."}, status=401
            )
        elif res == 2:
            return JsonResponse(
                {"message": "Token has expired."}, status=401
            )
        elif not request.user.is_admin:
            return JsonResponse(
                {"message": "User must be admin."}, status=401
            )
        else:
            response = func(self, request, *args, **kwargs)
            jwt = generate_jwt({"user_id": request.user.id,
                               "is_admin": request.user.is_admin})
            response.data['jwt'] = jwt
            return response

    return wrapper
