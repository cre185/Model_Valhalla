from django.db import models
from user import models as user

# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=127)
    data_file = models.FileField(upload_to='static/data', default='static/data/ceval_select.csv')
    add_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=user.User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name