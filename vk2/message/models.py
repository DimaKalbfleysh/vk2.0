from django.db import models

# Create your models here.
from django.utils import timezone
from account.models import Account


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
