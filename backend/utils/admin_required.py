from .jwt import *

def admin_required(func):
    # @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        jwt_authentication(request)
        if not request.user:
            return JsonResponse(
                {"message": "User must be authorized."}, status=401
            )
        elif not request.user.is_admin:
            return JsonResponse(
                {"message": "User must be admin."}, status=401
            )
        else:
            return func(self, request, *args, **kwargs)

    return wrapper

