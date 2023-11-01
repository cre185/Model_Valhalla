from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=255)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
    
class VerifyMsg(models.Model):
    mobile = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.mobile