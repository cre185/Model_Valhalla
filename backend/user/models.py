from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=11)
    add_time = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=255, null=True)
    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='avatar',
        default='media/avatar/default.jpg')


class VerifyMsg(models.Model):
    mobile = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(auto_now_add=True)


class VerifyEmail(models.Model):
    email = models.CharField(max_length=127)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(auto_now_add=True)


class LLMSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    llm = models.ForeignKey('testing.LLMs', on_delete=models.CASCADE)


class DatasetSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey('dataset.Dataset', on_delete=models.CASCADE)


class Msg(models.Model):
    msg = models.TextField(max_length=1000)
    msg_type = models.CharField(max_length=32)
    add_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author')
    msg_content = models.JSONField(default=dict)
    msg_file = models.FileField(upload_to='msg', null=True)
    target = models.ManyToManyField(
        User, related_name='target', through='MsgTarget')


class MsgTarget(models.Model):
    msg = models.ForeignKey(Msg, on_delete=models.CASCADE)
    target = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
