from django.db import models
from dataset import models as dataset
from testing import models as testing

# Create your models here.

class Credit(models.Model):
    dataset = models.ForeignKey(to=dataset.Dataset, on_delete=models.CASCADE)
    LLM = models.ForeignKey(to=testing.LLMs, on_delete=models.CASCADE)
    credit = models.FloatField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)