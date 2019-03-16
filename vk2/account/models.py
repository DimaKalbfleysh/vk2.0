""" All models in one application. It's wrong, I know. Soon correct."""
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from account.fields_with_choices import SEX_CHOICES, MARITAL_STATUS, BIRTH_DAY, MONTH_BIRTH, YEAR_BIRTH
from django.db.models import signals
from django.core.mail import send_mail
from register.tasks import send_verification_email


def user_directory_path(instance, filename):
    return 'images/id{0}/{1}'.format(instance.account.pk, filename)


class Account(User):
    is_another_user = models.BooleanField(blank=True, null=True)
    main_photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default='defult-photo.png')
    number_not_read_messages = models.IntegerField(null=True, default=0)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=False, null=True, default='Не выбрано')
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, blank=False, null=True,
                                      default='Не выбрано')
    birth_day = models.IntegerField(choices=BIRTH_DAY, blank=False, null=True, default='1')
    month_birth = models.CharField(max_length=20, choices=MONTH_BIRTH, blank=False, null=True, default='Января')
    year_birth = models.IntegerField(choices=YEAR_BIRTH, blank=False, null=True, default='2005')
    is_verified = models.BooleanField('verified', default=False) # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=Account)


class Group(models.Model):
    name = models.CharField(max_length=150, blank=False, null=True)
    status = models.CharField(max_length=150, blank=False, null=True)
    description = models.CharField(max_length=450, blank=False, null=True)
    web_site = models.CharField(max_length=150, blank=False, null=True)
    main_photo = models.ImageField(blank=True, null=True, default='defult-photo.png')
    header_photo = models.ImageField(blank=True, null=True, default=None)
    admin = models.ManyToManyField(Account, blank=True, related_name='group_for_admin')
    subscribers = models.ManyToManyField(Account, blank=True, related_name='group')
    count_subscribers = models.IntegerField(null=True, default=0)
    fixed_post = models.OneToOneField("Post", on_delete=models.CASCADE, blank=True, null=True, related_name='_group')


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='posts', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', null=True)
    pub_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    content = models.CharField(max_length=1500, blank=False, null=True)
    like_put = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ['-pub_date']


class Photo(models.Model):
    id_photo = models.IntegerField(null=True, unique=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default='defult-photo.png')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='images', null=True)
    post = models.ManyToManyField(Post, related_name='images', blank=True)
    like_put = models.BooleanField(null=True, default=False)

    def get_new_id_photo(self):
        return int(self.objects.all()[0].id_photo) + 1

    class Meta:
        ordering = ['-id']


class Dialog(models.Model):
    id_dialog = models.IntegerField(null=True, unique=True)
    users = models.ManyToManyField(Account, blank=True, related_name='dialogs')
    interlocutor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='dialogs_for_interlocutor',
                                     null=True)
    pub_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    number_not_read_messages = models.IntegerField(null=True)

    def set_pub_date(self):
        self.pub_date = self.messages.last().pub_date
        self.save()

    def set_interlocutor(self, main_user):
        for user in self.users.all():
            if user != main_user:
                self.interlocutor = user
                self.save()

    def count_not_read_messages(self):
        self.number_not_read_messages = 0
        for message in self.messages.all():
            if not message.is_read:
                self.number_not_read_messages += 1
        self.save()


class GroupMessages(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='group_messages', null=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='group_messages', null=True)
    pub_date = models.DateTimeField(blank=False, null=True, default=timezone.now)


class Message(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='messages', null=True)
    message = models.CharField(max_length=150, blank=True, null=True)
    group_messages = models.ForeignKey(GroupMessages, on_delete=models.CASCADE, related_name='messages', null=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages', null=True)
    pub_date = models.DateTimeField(blank=False, null=True, default=timezone.now)
    is_read = models.BooleanField(blank=False, null=True, default=False)

    def set_read(self, main_user):
        main_user.number_not_read_messages -= 1
        self.is_read = True
        main_user.save()
        self.save()


class Audio(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='audios', blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='likes', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)


class Views(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='views', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views', blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='views', blank=True, null=True)
