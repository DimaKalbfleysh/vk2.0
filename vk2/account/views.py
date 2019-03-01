from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from account.models import Account
from friendship.models import Friend
from friendship.models import FriendshipRequest
from account.models import Photo
from account.models import Massage
from account.models import Dialog
from account.models import Post
import random


def get_all_friends(user):
    """ Since there are no fields in the main User model that will be useful for us in the template, we convert each 
    friend to the Account model we created """
    all_friends = []
    for friend in Friend.objects.friends(user):
        converted_friend = Account.objects.get(pk=friend.pk)
        all_friends.append(converted_friend)
    return all_friends


def get_friends_row(all_friends):
    random.shuffle(all_friends)
    if len(all_friends) <= 3:
        friends_row = [all_friends[-3:]]
    else:
        friends_row_one = all_friends[-3:]
        friends_row_two = all_friends[:3]
        friends_row = [friends_row_one, friends_row_two]
    return friends_row


class MainView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            main_user = Account.objects.get(pk=request.user.pk)
            print(main_user.count_not_readed_massages)
            user = Account.objects.get(pk=pk)
            posts = user.posts.all()
            main_photo = list(user.images.all())[0]
            user.main_photo = main_photo.photo
            all_photo = list(user.images.all())[:3]
            count_photo = len(user.images.all())
            request_is_send = Friend.objects.can_request_send(request.user, user)
            accept_request = Friend.objects.can_request_send(user, request.user)
            is_friend = Friend.objects.are_friends(request.user, user)
            user.is_another_user = (int(pk) != int(request.user.pk))
            user.save()
            all_friends = get_all_friends(user)
            friends_row = get_friends_row(all_friends)
            count_friends = len(all_friends)
            if request.GET.get('friendship') == 'request':
                Friend.objects.add_friend(request.user, user)
                return redirect('account', pk=user.pk)

            if request.GET.get('friendship') == 'accept':
                friend_request = FriendshipRequest.objects.get(from_user=pk, to_user=request.user.pk)
                friend_request.accept()
                return redirect('account', pk=pk)
            context = dict()
            context['user'] = user
            context['main_user'] = main_user
            context['request_is_send'] = request_is_send
            context['accept_request'] = accept_request
            context['is_friend'] = is_friend
            context['all_photo'] = all_photo
            context['count_photo'] = count_photo
            context['all_friends'] = all_friends
            context['friends_row'] = friends_row
            context['count_friends'] = count_friends
            context['posts'] = posts
            return render(request, 'account/user_account.html', context=context)
        else:
            return redirect('login')


class AlbumsView(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        all_photo = user.images.all()
        count_photo = len(all_photo)
        context = dict()
        context['user'] = user
        context['main_user'] = main_user
        context['all_photo'] = all_photo
        context['count_photo'] = count_photo
        return render(request, 'account/albums.html', context=context)


class FriendsView(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        all_friends = get_all_friends(user)
        context = dict()
        context['user'] = user
        context['main_user'] = main_user
        context['all_friends'] = all_friends
        context['count_friends'] = len(all_friends)
        return render(request, 'account/friends.html', context=context)


class DialogView(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        dialogs = main_user.dialogs.all()
        for dialog in dialogs:
            for user in dialog.users.all():
                if user != main_user:
                    dialog.interlocutor = user
                    dialog.save()
        context = dict()
        context['dialogs'] = dialogs
        context['main_user'] = main_user
        context['url'] = request.get_full_path()
        return render(request, 'account/dialogs.html', context=context)


def create_dialog(main_user, interlocutor):
    k = 0
    for dialog in main_user.dialogs.all():
        if interlocutor != dialog.users.all()[0] and interlocutor != dialog.users.all()[1]:
            k += 1

    if k == len(main_user.dialogs.all()):
        dialog = Dialog.objects.create(id_dialog=main_user.pk + interlocutor.pk)
        dialog.users.add(main_user, interlocutor)


class MassageView(View):
    def get(self, request):
        pk = request.GET['sel']
        main_user = Account.objects.get(pk=request.user.pk)
        interlocutor = Account.objects.get(pk=pk)
        create_dialog(main_user, interlocutor)
        dialogs = main_user.dialogs.all()
        for dialog in dialogs:
            for user in dialog.users.all():
                if user != main_user:
                    dialog.interlocutor = user
                    dialog.save()
        dialog = main_user.dialogs.get(id_dialog=main_user.pk + interlocutor.pk)
        massages = dialog.massages.all()
        for massage in massages:
            if not massage.is_readed:
                main_user.count_not_readed_massages -= 1
                massage.is_readed = True
                main_user.save()
                massage.save()
        return render(request, 'account/massages.html', context={'main_user': main_user,
                                                                 'to_user': interlocutor,
                                                                 'massages': massages,
                                                                 'url': request.get_full_path().split('?')[0]})

    def post(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        to_user = Account.objects.get(pk=request.GET['sel'])
        to_user.save()
        dialog = main_user.dialogs.get(id_dialog=main_user.pk + to_user.pk)
        Massage.objects.create(massage=request.POST['massage'], dialog=dialog, author=main_user)
        return JsonResponse({})


class UpdateMassagesView(View):
    def get(self, request):
        if 'sel' in request.GET:
            pk = request.GET['sel']
            main_user = Account.objects.get(pk=request.user.pk)
            interlocutor = Account.objects.get(pk=pk)
            dialog = main_user.dialogs.get(id_dialog=main_user.pk + interlocutor.pk)
            massages = list(dialog.massages.all())
            massages_values = list(dialog.massages.all().values())
            data = dict()
            data['massages'] = massages_values
            data['first_name'] = massages[-1].author.first_name
            data['url_photo'] = massages[-1].author.main_photo.url
            data['pub_time'] = massages[-1].pub_date.time()
            return JsonResponse(data)
        elif 'cou' in request.GET:
            main_user = Account.objects.get(pk=request.user.pk)
            dialogs = main_user.dialogs.all()
            count_not_readed_massages = 0
            for dialog in dialogs:
                for user in dialog.users.all():
                    if user != main_user:
                        massages = dialog.massages.filter(author=user)
                        for massage in massages:
                            if not massage.is_readed:
                                count_not_readed_massages += 1
            main_user.count_not_readed_massages = count_not_readed_massages
            main_user.save()
            print(main_user.count_not_readed_massages)
            data = dict()
            data['count_not_readed_massages'] = count_not_readed_massages
            return JsonResponse(data)


class PostView(View):
    def get(self, request):
        pass

    def post(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        content = request.POST['content']
        photo1 = Photo.objects.all()[5]
        photo2 = Photo.objects.all()[4]
        post = Post.objects.create(author=main_user, content=content)
        post.images.add(photo1, photo2)
        return JsonResponse({})
