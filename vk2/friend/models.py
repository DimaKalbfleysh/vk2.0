from django.db import models

# Create your models here.
from account.models import Account


class Friend(models.Model):
    users = models.ManyToManyField(Account, related_name='friend', blank=True)
    who = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='who_friend', null=True)


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friendship_from_user', null=True)
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friendship_to_user', null=True)
    is_accept = models.BooleanField(default=False)