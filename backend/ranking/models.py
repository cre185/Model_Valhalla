from django.db import models
from user import models as user
from dataset import models as dataset
from testing import models as testing

# Create your models here.

class Credit(models.Model):
    dataset = models.ForeignKey(to=dataset.Dataset, on_delete=models.CASCADE)
    LLM = models.ForeignKey(to=testing.LLMs, on_delete=models.CASCADE)
    credit = models.IntegerField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)

class DatasetComment(models.Model):
    dataset = models.ForeignKey(to=dataset.Dataset, on_delete=models.CASCADE)
    respond_to = models.IntegerField(null=True)
    like = models.ManyToManyField(to=user.User, through='DatasetLike', related_name='dataset_comment_like')
    user = models.ForeignKey(to=user.User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

class DatasetLike(models.Model):
    comment = models.ForeignKey(to=DatasetComment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=user.User, on_delete=models.SET_NULL, null=True)
    dislike = models.BooleanField(default=False)

class LLMComment(models.Model):
    llm = models.ForeignKey(to=testing.LLMs, on_delete=models.CASCADE)
    respond_to = models.IntegerField(null=True)
    like = models.ManyToManyField(to=user.User, through='LLMLike', related_name='llm_comment_like')
    user = models.ForeignKey(to=user.User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

class LLMLike(models.Model):
    comment = models.ForeignKey(to=LLMComment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=user.User, on_delete=models.SET_NULL, null=True)
    dislike = models.BooleanField(default=False)