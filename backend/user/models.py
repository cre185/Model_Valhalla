from django.db import models
from testing.models import LLMs

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=11)
    add_time = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=255, null=True)
    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='static/avatar', default='static/avatar/default.jpg')
    subscribed_llm = models.ManyToManyField(LLMs, through='Subscription')
    def __str__(self):
        return self.username
    
class VerifyMsg(models.Model):
    mobile = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.mobile

class VerifyEmail(models.Model):
    email = models.CharField(max_length=127)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    llm = models.ForeignKey(LLMs, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + " " + self.llm.name