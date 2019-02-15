from django.db import models


# Create your models here.
class Post(models.Model):
    body = models.TextField(blank=True, db_index=True)
    img = models.ImageField(blank=True, max_length=10000)
