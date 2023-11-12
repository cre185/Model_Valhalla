from .settings import *

DEBUG = False

ALLOWED_HOSTS =  ['localhost', '127.0.0.1']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "model_valhalla",
        "USER": "root",
        "PASSWORD": "20231112",
        "HOST": "mysql",
        "PORT": "3306",
    }
}
