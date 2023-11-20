from django.db import models
from Model_Valhalla.settings import GPT_KEY
# Create your models here.

class LLMs(models.Model):
    name = models.CharField(max_length=127)
    api_url = models.CharField(max_length=255, default='https://api.openai.com/v1/chat/completions')
    api_headers = models.TextField(default='{"Authorization":"Bearer '+GPT_KEY+'"}')
    api_data = models.TextField(default='{"model": "gpt-3.5-turbo","messages": [{"role": "user", "content": "$PROMPT"}],"temperature": 0.7}')
    api_RPM = models.IntegerField(null=True, default=3)
    logo = models.ImageField(upload_to='static/logo', default='static/logo/default.jpg')
    official_website = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    document_name = models.TextField(default='')
    document_website = models.TextField(default='')
    license = models.TextField(default='')
    elo_credit = models.FloatField(default=1500)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

