from django.db import models

# Create your models here.

class LLMs(models.Model):
    name = models.CharField(max_length=127)
    add_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name