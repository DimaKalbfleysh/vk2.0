""" All models in one application. It's wrong, I know. Soon correct."""
import uuid
from django.db import models
from django.contrib.auth.models import User
from account.fields_with_choices import SEX_CHOICES, MARITAL_STATUS, BIRTH_DAY, MONTH_BIRTH, YEAR_BIRTH
from django.db.models import signals
# from register.tasks import send_verification_email


def user_directory_path(instance, filename):
    return 'images/id{0}/{1}'.format(instance.account.pk, filename)


class Account(User):
    is_another_user = models.BooleanField(blank=True, null=True)
    main_photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default='defult-photo.png')
    number_not_read_messages = models.IntegerField(null=True, default=0)
    sex = models.CharField(max_length=1000, choices=SEX_CHOICES, blank=False, null=True, default='Не выбрано')
    marital_status = models.CharField(max_length=2000, choices=MARITAL_STATUS, blank=False, null=True,
                                      default='Не выбрано')
    birth_day = models.IntegerField(choices=BIRTH_DAY, blank=False, null=True, default='1')
    month_birth = models.CharField(max_length=2000, choices=MONTH_BIRTH, blank=False, null=True, default='Января')
    year_birth = models.IntegerField(choices=YEAR_BIRTH, blank=False, null=True, default='2005')
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    unrejected_request_number = models.IntegerField(null=True, default=0)
    number_friends = models.IntegerField(null=True, default=0)


# def user_post_save(sender, instance, signal, *args, **kwargs):
#     if not instance.is_verified:
#         send_verification_email.delay(instance.pk)
#
#
# signals.post_save.connect(user_post_save, sender=Account)

