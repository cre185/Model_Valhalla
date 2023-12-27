from django.db import models

from user.models import User

# Create your models here.


class Dataset(models.Model):
    name = models.CharField(max_length=127)
    data_file = models.FileField(
        upload_to='static/data',
        null=True)
    content_size = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='')
    subjective = models.BooleanField(default=False)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    domain = models.CharField(max_length=127, default='')
    tag = models.JSONField(default=list)
