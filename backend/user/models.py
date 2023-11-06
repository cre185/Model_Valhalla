from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=11)
    add_time = models.DateTimeField(auto_now_add=True)
    # email_address = models.CharField(max_length=100)  #
    # email_verifycode = models.CharField(max_length=255, unique=False, null=True)  # 验证码
    # email_verifycode_time = models.CharField(max_length=255, unique=False, default=time.time())# 验证码的发送时间
    def __str__(self):
        return self.username
    
class VerifyMsg(models.Model):
    mobile = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.mobile
