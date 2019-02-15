import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from account.models import Account
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from friendship.models import Friend
from friendship.models import FriendshipRequest
from account.models import Photo
from django_ajax.decorators import ajax
from django_ajax.mixin import AJAXMixin
from account.models import Massage

from account.models import Dialog


class MainView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            main_user = Account.objects.get(pk=request.user.pk)
            user = Account.objects.get(pk=pk)
            main_photo = list(user.images.all())[0]
            user.main_photo = main_photo.photo
            all_photo = list(user.images.all())[:3]
            count_photo = len(user.images.all())
            request_is_send = Friend.objects.can_request_send(request.user, user)
            accept_request = Friend.objects.can_request_send(user, request.user)
            is_friend = Friend.objects.are_friends(request.user, user)
            user.is_another_user = (int(pk) != int(request.user.pk))
            user.save()
            all_friends = Friend.objects.friends(user)
            count_friends = len(all_friends)
            if request.GET.get('friendship') == 'request':
                Friend.objects.add_friend(request.user, user, message='Hi! I would like to add you')
                return redirect('account', pk=user.pk)

            if request.GET.get('friendship') == 'accept':
                friend_request = FriendshipRequest.objects.get(from_user=pk, to_user=request.user.pk)
                friend_request.accept()
                return redirect('account', pk=pk)
            context = {'user': user,
                       'main_user': main_user,
                       'request_is_send': request_is_send,
                       'accept_request': accept_request,
                       'is_friend': is_friend,
                       'all_photo': all_photo,
                       'count_photo': count_photo,
                       'all_friends': all_friends,
                       'count_friends': count_friends}
            return render(request, 'account/user_account.html', context=context)
        else:
            return redirect('login')


class AlbumsView(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        all_photo = user.images.all()
        count_photo = len(all_photo)
        all_friends = Friend.objects.friends(user)
        count_friends = len(all_friends)
        return render(request, 'account/albums.html', context={'user': user,
                                                               'main_user': main_user,
                                                               'all_photo': all_photo,
                                                               'count_photo': count_photo,
                                                               'all_friends': all_friends,
                                                               'count_friends': count_friends})


class FriendsView(View):
    # template_name = 'account/friends.html'
    #
    # def get_context_data(self, **kwargs):
    #     print(self.request.is_ajax())
    #     context = super(FriendsView, self).get_context_data(**kwargs)
    #     context['main_user'] = Account.objects.get(pk=self.request.user.pk)
    #     user = Account.objects.get(pk=self.request.user.pk)
    #     context['user'] = user
    #     all_friends = []
    #     for i in Friend.objects.friends(user):
    #         a = Account.objects.get(pk=i.pk)
    #         all_friends.append(a)
    #     context['all_friends'] = all_friends
    #     context['count_friends'] = len(all_friends)
    #     return context

    def get(self, request, pk):
        print(request.is_ajax())
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        all_friends = []
        for i in Friend.objects.friends(user):
            a = Account.objects.get(pk=i.pk)
            all_friends.append(a)
        count_friends = len(all_friends)
        return render(request, 'account/friends.html', context={'user': user,
                                                                'main_user': main_user,
                                                                'all_friends': all_friends,
                                                                'count_friends': count_friends})


class DialogView(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        dialogs = main_user.dialogs.all()
        for dialog in dialogs:
            for user in dialog.users.all():
                if user != main_user:
                    dialog.interlocutor = user
                    dialog.save()
        return render(request, 'account/dialogs.html', context={'main_user': main_user,
                                                                'dialogs': dialogs})


class MassageView(View):
    def get(self, request):
        pk = request.GET['sel']
        main_user = Account.objects.get(pk=request.user.pk)
        to_user = Account.objects.get(pk=pk)
        k = 0
        for dialog in main_user.dialogs.all():
            if to_user != dialog.users.all()[0] and to_user != dialog.users.all()[1]:
                k += 1

        if k == len(main_user.dialogs.all()):
            dialog = Dialog.objects.create(id_dialog=main_user.pk+to_user.pk)
            dialog.users.add(main_user, to_user)

        massages = to_user.dialogs.get(id_dialog=main_user.pk+to_user.pk).massages.all()
        return render(request, 'account/massages.html', context={'main_user': main_user,
                                                                 'to_user': to_user,
                                                                 'massages': massages})

    def post(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        to_user = Account.objects.get(pk=request.GET['sel'])
        dialog = main_user.dialogs.get(id_dialog=main_user.pk + to_user.pk)
        massage = Massage.objects.create(massage=request.POST['massage'],
                                         dialog=dialog, author=main_user)
        return JsonResponse({'massage': massage.massage})

        # if request.GET and int(request.GET['sel']) == 35:
        #     return render(request, 'account/massages.html', context={'main_user': main_user})
        # if request.is_ajax():
        #     print(0)
        #     massage = Massage.objects.create(massage=request.GET['massage'])
        #     print(massage.massage, 1)
        #     from_user = Account.objects.get(pk=request.user.pk)
        #     print(from_user, 2)
        #     to_user = Account.objects.get(pk=request.GET['user_pk'])
        #     print(to_user, 3)
        #     massage.from_user = from_user
        #     massage.to_user = to_user
        #     massage.save()
        #     print(massage.to_user, 4)
        #     from_user.massage_from_user.add(massage)
        #     to_user.massage_to_user.add(massage)
        #     print(1)
        #     return JsonResponse({'massage_from_user': massage.massage,
        #                          'massage_to_user': massage.massage})
