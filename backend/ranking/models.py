from django.db import models
from dataset import models as dataset
from testing import models as testing

# Create your models here.

class Credit(models.Model):
    dataset = models.ForeignKey(to=dataset.Dataset, on_delete=models.DO_NOTHING)
    LLM = models.ForeignKey(to=testing.LLMs, on_delete=models.DO_NOTHING)
    credit = models.FloatField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)