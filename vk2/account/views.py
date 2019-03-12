from django.shortcuts import render, redirect
from django.views import View
from account.models import Account, Store, Purchase
from friendship.models import Friend
from friendship.models import FriendshipRequest
import random
from django.db.models import Count, F

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
