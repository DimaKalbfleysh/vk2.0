from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from account.models import Account
from friendship.models import Friend
from friendship.models import FriendshipRequest
from account.models import Photo
from account.models import Message
from account.models import Dialog
from account.models import Post, Group, Like, GroupMessages
import random
from edit.forms import PhotoForm


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
            user = Account.objects.get(pk=pk)
            posts = user.posts.all()
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
        photo_form = PhotoForm(instance=main_user)
        user = Account.objects.get(pk=pk)
        all_photo = user.images.all()
        count_photo = len(all_photo)
        context = dict()
        context['user'] = user
        context['main_user'] = main_user
        context['all_photo'] = all_photo
        context['count_photo'] = count_photo
        context['photo_form'] = photo_form
        return render(request, 'account/albums.html', context=context)

    def post(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        new_photo = Photo.objects.create(photo=request.FILES['photo'], account=main_user)
        main_user.images.add(new_photo)
        return redirect('albums', pk=main_user.pk)


class DeletePhotoView(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        photo = main_user.images.get(pk=request.GET['pk'])
        photo.delete()
        return JsonResponse({})


class MakeMainPhoto(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        main_photo = Photo.objects.get(pk=request.GET['pk'])
        main_user.main_photo = main_photo.photo
        main_user.save()
        return JsonResponse({})


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


class MessageView(View):
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
        groups_messages = dialog.group_messages.all()
        for group_messages in groups_messages:
            for message in group_messages.messages.all():
                if not message.is_readed:
                    main_user.count_not_readed_messages -= 1
                    message.is_readed = True
                    main_user.save()
                    message.save()
        return render(request, 'account/messages.html', context={'main_user': main_user,
                                                                 'to_user': interlocutor,
                                                                 'groups_messages': groups_messages,
                                                                 'url': request.get_full_path().split('?')[0]})

    def post(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        to_user = Account.objects.get(pk=request.GET['sel'])
        to_user.save()
        dialog = main_user.dialogs.get(id_dialog=main_user.pk + to_user.pk)
        message = Message.objects.create(message=request.POST['message'], dialog=dialog, author=main_user)
        if not dialog.group_messages.filter(user=main_user).last():
            group_messages = GroupMessages.objects.create(user=main_user, dialog=dialog)
            group_messages.messages.add(message)
            return JsonResponse({})
        else:
            group_messages = dialog.group_messages.last()
            if group_messages.user == main_user:
                difference = ((message.pub_date - group_messages.messages.last().pub_date).seconds % 3600) // 60
            else:
                group_messages = GroupMessages.objects.create(user=main_user, dialog=dialog)
                group_messages.messages.add(message)
                return JsonResponse({})

        if difference > 5:
            group_messages = GroupMessages.objects.create(user=main_user, dialog=dialog)
            group_messages.messages.add(message)
            return JsonResponse({})
        group_messages.messages.add(message)
        return JsonResponse({})


class UpdateMessagesView(View):
    def get(self, request):
        if 'sel' in request.GET:
            pk = request.GET['sel']
            main_user = Account.objects.get(pk=request.user.pk)
            interlocutor = Account.objects.get(pk=pk)
            dialog = main_user.dialogs.get(id_dialog=main_user.pk + interlocutor.pk)
            messages = dialog.messages.all()
            messages_values = list(dialog.messages.all().values())
            data = dict()
            data['messages'] = messages_values
            data['first_name'] = messages.last().author.first_name
            data['url_photo'] = messages.last().author.main_photo.url
            data['pub_time'] = messages.last().pub_date.time()
            return JsonResponse(data)
        elif 'cou' in request.GET:
            main_user = Account.objects.get(pk=request.user.pk)
            dialogs = main_user.dialogs.all()
            count_not_readed_messages = 0
            for dialog in dialogs:
                for user in dialog.users.all():
                    if user != main_user:
                        messages = dialog.messages.filter(author=user)
                        for message in messages:
                            if not message.is_readed:
                                count_not_readed_messages += 1
            main_user.count_not_readed_messages = count_not_readed_messages
            main_user.save()
            print( count_not_readed_messages)
            data = dict()
            data['count_not_readed_messages'] = count_not_readed_messages
            return JsonResponse(data)


class PostView(View):
    def post(self, request):
        if request.POST['url'] == '/id{}/'.format(request.user.pk):
            main_user = Account.objects.get(pk=request.user.pk)
            content = request.POST['content']
            photo1 = Photo.objects.all()[5]
            photo2 = Photo.objects.all()[4]
            post = Post.objects.create(author=main_user, content=content)
            post.images.add(photo1, photo2)
            return JsonResponse({})
        if request.POST['url'] == '/public{}/'.format(request.POST['public_pk']):
            group = Group.objects.get(pk=request.POST['public_pk'])
            content = request.POST['content']
            photo1 = Photo.objects.all()[5]
            photo2 = Photo.objects.all()[4]
            post = Post.objects.create(group=group, content=content)
            post.images.add(photo1, photo2)
            return JsonResponse({})


class DeletePostView(View):
    def get(self, request):
        post = Post.objects.get(pk=request.GET['pk'])
        post.delete()
        return JsonResponse({})


class GroupsView(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        groups = Group.objects.all()
        return render(request, 'account/groups.html', context={'main_user': main_user, 'groups': groups})


class GroupView(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        group = Group.objects.get(pk=pk)
        posts = group.posts.all()
        for post in posts:
            if post.fixed_post:
                fixed_post = post
                break
        else:
            fixed_post = None
        return render(request, 'account/public.html', context={'main_user': main_user,
                                                               'group': group,
                                                               'posts': posts,
                                                               'fixed_post': fixed_post})


class PutLikePost(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        post = Post.objects.get(pk=request.GET['pk'])
        try:
            like = post.likes.get(user=main_user)
            like.delete()
            count_likes = post.likes.all().count()
            likes_put = False
        except:
            like = Like.objects.create(user=main_user, post=post)
            main_user.likes.add(like)
            post.likes.add(like)
            count_likes = post.likes.all().count()
            likes_put = True
        return JsonResponse({'likes_put': likes_put,
                             'count_likes': count_likes})


class PutLikePhoto(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        photo = Photo.objects.get(pk=request.GET['pk'])
        try:
            like = photo.likes.get(user=main_user)
            like.delete()
            count_likes = photo.likes.all().count()
            photo.like_put = False
            photo.save()
        except:
            like = Like.objects.create(user=main_user, photo=photo)
            main_user.likes.add(like)
            photo.likes.add(like)
            count_likes = photo.likes.all().count()
            photo.like_put = True
            photo.save()
        return JsonResponse({'likes_put': photo.like_put,
                             'count_likes': count_likes})
