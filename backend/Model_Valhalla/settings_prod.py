from .settings import *
DEBUG = False

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
