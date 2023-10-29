from django.db import models

# Create your models here.

class Response(models.Model):
    Case_id = models.IntegerField()
    Message = models.CharField(max_length=50)
    Added = models.DateTimeField(auto_now_add=True,)
