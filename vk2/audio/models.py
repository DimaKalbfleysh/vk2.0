from django.db import models

# Create your models here.
from post.models import Post


class Audio(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='audios', blank=True, null=True)