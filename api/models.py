from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length = 255, blank=False, null = False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    

