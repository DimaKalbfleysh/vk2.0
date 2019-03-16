import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from vk2.celery import app


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your Vk2 account',
            'Follow this link to verify your account: '
            'http://localhost:8000/verify'+user_id,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
