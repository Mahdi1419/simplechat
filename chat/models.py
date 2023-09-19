from django.db import models
from django.contrib.auth import get_user_model
import uuid
# Create your models here.

class Topic(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(get_user_model())
    


class Message(models.Model):
    text = models.TextField(max_length=1024)
    sender = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)
    # message_type = 
