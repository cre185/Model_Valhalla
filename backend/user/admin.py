from django.contrib import admin

from .models import User, VerifyMsg

# Register your models here.
admin.site.register(User)
admin.site.register(VerifyMsg)