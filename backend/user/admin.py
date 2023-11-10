from django.contrib import admin

from .models import User, VerifyMsg, VerifyEmail

# Register your models here.
admin.site.register(User)
admin.site.register(VerifyMsg)
admin.site.register(VerifyEmail)