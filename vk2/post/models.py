from django.db import models
from account.models import Account
from django.utils import timezone
from group.models import Group


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='posts', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', null=True)
    pub_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    content = models.CharField(max_length=1500, blank=False, null=True)
    like_put = models.BooleanField(null=True, default=False)
    who_liked = models.ManyToManyField(Account, related_name='post', blank=True)

    class Meta:
        ordering = ['-pub_date']