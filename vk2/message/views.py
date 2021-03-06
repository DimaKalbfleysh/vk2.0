from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from account.models import Account
from message.models import Dialog, Message, GroupMessages


class DialogsView(View):
    def get(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        dialogs = main_user.dialogs.all()

        for dialog in dialogs:
            dialog.set_pub_date()
            dialog.set_interlocutor(main_user)

        context = dict()
        context['dialogs'] = dialogs.order_by('-pub_date')
        context['main_user'] = main_user
        context['url'] = request.get_full_path()
        return render(request, 'message/dialogs.html', context=context)


def create_dialog(main_user, interlocutor):
    count_dialogs_without_interlocutor = 0
    for dialog in main_user.dialogs.all():
        if interlocutor not in dialog.users.all():
            count_dialogs_without_interlocutor += 1

    if count_dialogs_without_interlocutor == main_user.dialogs.count():
        dialog = Dialog.objects.create(id_dialog=main_user.pk + interlocutor.pk)
        dialog.users.add(main_user, interlocutor)


class MessagesView(View):
    def get(self, request):
        pk = request.GET['sel']
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        interlocutor = Account.objects.select_related().get(pk=pk)
        create_dialog(main_user, interlocutor)
        dialogs = main_user.dialogs.all()

        for dialog in dialogs:
            dialog.set_interlocutor(main_user)

        dialog = main_user.dialogs.get(id_dialog=main_user.pk + interlocutor.pk)

        for message in dialog.messages.all():
            if message.author != main_user:
                if not message.is_read:
                    message.set_read(main_user)

        context = dict()
        context['main_user'] = main_user
        context['to_user'] = interlocutor
        context['dialog'] = dialog
        context['url'] = request.get_full_path().split('?')[0]
        return render(request, 'message/messages.html', context=context)

    def post(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        to_user = Account.objects.select_related().get(pk=request.GET['sel'])
        dialog = main_user.dialogs.get(id_dialog=main_user.pk + to_user.pk)
        created_message = Message.objects.create(message=request.POST['message'], dialog=dialog, author=main_user)

        # if the dialog is not empty and the last message is from main_user then:
        if dialog.group_messages.filter(user=main_user).last() and dialog.group_messages.last().user == main_user:
            group_messages = dialog.group_messages.last()  # get last group_messages in dialog
            last_message = group_messages.messages.last()  # get last message in group_messages
            difference = ((created_message.pub_date - last_message.pub_date).seconds % 3600) // 60  # get the difference in sending date between created_message and last_message in minutes
        else:
            group_messages = GroupMessages.objects.create(user=main_user, dialog=dialog)
            group_messages.messages.add(created_message)
            return JsonResponse({})

        #  if the difference is more than 5 minutes
        if difference > 5:
            group_messages = GroupMessages.objects.create(user=main_user, dialog=dialog)
            group_messages.messages.add(created_message)
            return JsonResponse({})
        group_messages.messages.add(created_message)
        return JsonResponse({})


class UpdateMessagesView(View):
    def get(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        interlocutor = Account.objects.get(pk=request.GET['sel'])
        dialog = main_user.dialogs.get(id_dialog=main_user.pk + interlocutor.pk)
        messages = dialog.messages.select_related()
        for message in messages:
            if message.author != main_user:
                if not message.is_read:
                    message.set_read(main_user)
        messages_values = list(messages.values())
        data = dict()
        data['messages'] = messages_values
        data['first_name'] = messages.last().author.first_name
        data['url_photo'] = messages.last().author.main_photo.url
        data['pub_time'] = messages.last().pub_date.time()
        return JsonResponse(data)


class UpdateDialogsView(View):
    def get(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        dialogs = main_user.dialogs.filter(messages__is_read=False).exclude(messages__author=main_user).annotate(count_messages=Count('messages'))
        number_not_read_messages = 0
        for dialog in dialogs:
            number_not_read_messages += dialog.count_messages

        main_user.number_not_read_messages = number_not_read_messages
        main_user.save()
        data = dict()
        data['number_not_read_messages'] = number_not_read_messages
        data['dialogs_values'] = list(dialogs.values())
        return JsonResponse(data)

