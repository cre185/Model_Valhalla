from django.db import models

# Create your models here.


class LLMs(models.Model):
    name = models.CharField(max_length=127)
    api_url = models.CharField(
        max_length=255,
        default='http://111.202.73.146:10510/v1/chat/completions')
    model_name = models.CharField(max_length=255, default='mistral_7b')
    api_RPM = models.IntegerField(null=True)
    logo = models.ImageField(
        upload_to='logo',
        default='media/logo/default.jpg')
    official_website = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    document_name = models.TextField(default='')
    document_website = models.TextField(default='')
    license = models.TextField(default='')
    elo_credit = models.FloatField(default=1500)
    add_time = models.DateTimeField(auto_now_add=True)
    released_time = models.CharField(max_length=255, default='')


class BattleHistory(models.Model):
    llm1 = models.ForeignKey(
        LLMs,
        on_delete=models.CASCADE,
        related_name='llm1')
    llm2 = models.ForeignKey(
        LLMs,
        on_delete=models.CASCADE,
        related_name='llm2')
    round = models.IntegerField()
    result = models.JSONField()
    user_id = models.IntegerField()
    winner = models.IntegerField()
    add_time = models.DateTimeField(auto_now_add=True)
