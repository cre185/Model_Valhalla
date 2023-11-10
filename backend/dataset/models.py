from django.db import models

# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=127)
    data_file = models.FileField(upload_to='static/data', null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name