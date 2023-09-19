from django.contrib import admin
from .models import Message, Topic

# Register your models here.
admin.site.register((Topic, Message))