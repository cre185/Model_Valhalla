from django.db import models

# Create your models here.

class LLMs(models.Model):
    name = models.CharField(max_length=127)
    api_url = models.CharField(max_length=255, default='https://api.openai.com/v1/chat/completions')
    api_headers = models.TextField(default='{"Authorization":"Bearer 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"}')
    api_data = models.TextField(default='{"model": "gpt-3.5-turbo","messages": [{"role": "user", "content": "$PROMPT"}],"temperature": 0.7}')
    api_RPM = models.IntegerField(null=True, default=3)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    