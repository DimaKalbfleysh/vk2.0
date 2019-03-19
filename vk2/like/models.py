from django.db import models
from account.models import Account
from photo.models import Photo
from post.models import Post


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='likes', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)


class Views(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='views', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views', blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='views', blank=True, null=True)
