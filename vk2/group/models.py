from django.db import models
from account.models import Account


class Group(models.Model):
    name = models.CharField(max_length=150, blank=False, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=450, blank=True, null=True)
    web_site = models.CharField(max_length=150, blank=True, null=True)
    main_photo = models.ImageField(blank=True, null=True, default='defult-photo.png')
    header_photo = models.ImageField(blank=True, null=True, default=None)
    admin = models.ManyToManyField(Account, blank=False, related_name='group_for_admin')
    subscribers = models.ManyToManyField(Account, blank=True, related_name='group')
    number_subscribers = models.IntegerField(null=True, default=0)
    fixed_post = models.OneToOneField('post.Post', on_delete=models.CASCADE, blank=True, null=True, related_name='_group')

    def count_subscribers(self):
        self.number_subscribers = self.subscribers.count()
        self.save()
        return self.number_subscribers


