from django.contrib import admin

from .models import User, VerifyEmail, VerifyMsg

# Register your models here.
admin.site.register(User)
admin.site.register(VerifyMsg)
admin.site.register(VerifyEmail)