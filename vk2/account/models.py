from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def user_directory_path(instance, filename):
    return 'images/id{0}/{1}'.format(instance.account.pk, filename)


class Account(User):
    is_another_user = models.BooleanField(blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="DOB", blank=True, null=True)
    main_photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default='defult-photo.png')


class Photo(models.Model):
    id_photo = models.IntegerField(null=True, unique=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default='defult-photo.png')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='images', null=True)

    class Meta:
        ordering = ['-id']


class Dialog(models.Model):
    id_dialog = models.IntegerField(null=True, unique=True)
    users = models.ManyToManyField(Account, blank=True, related_name='dialogs')
    interlocutor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='dialogs_for_interlocutor', null=True)


class Massage(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='massages', null=True)
    massage = models.CharField(max_length=150, blank=True, null=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='massages', null=True)
    pub_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    is_readed = models.BooleanField(blank=False, null=True, default=False)
