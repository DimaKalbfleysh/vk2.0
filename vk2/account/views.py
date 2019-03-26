from django.shortcuts import render, redirect
from django.views import View
from account.models import Account
from friend.models import FriendshipRequest, Friend
import random
from django.db.models import Q


def get_friends_row(all_friends):
    random.shuffle(all_friends)
    if len(all_friends) <= 3:
        friends_row = [all_friends[-3:]]
    else:
        friends_row_one = all_friends[-3:]
        friends_row_two = all_friends[:3]
        friends_row = [friends_row_one, friends_row_two]
    return friends_row


class MainPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account', pk=request.user.pk)
        return redirect('login')


class MainView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            main_user = Account.objects.select_related().get(pk=request.user.pk)
            if int(request.user.pk) != int(pk):
                user = Account.objects.select_related().get(pk=pk)
                try:
                    friendship_request = FriendshipRequest.objects.get(Q(from_user=main_user, to_user=user)|Q(from_user=user, to_user=main_user))
                except:
                    friendship_request = None
            else:
                user = main_user
                friendship_request = None
            posts = user.posts.all()
            all_photo = list(user.images.all())[:3]
            count_photo = user.images.count()
            user.is_another_user = (int(pk) != int(request.user.pk))
            user.save()
            all_friends = Friend.objects.get(who=user).users.all()
            friends_row = get_friends_row(list(all_friends))
            count_friends = all_friends.count()
            context = dict()
            context['user'] = user
            context['main_user'] = main_user
            context['friendship_request'] = friendship_request
            context['all_photo'] = all_photo
            context['count_photo'] = count_photo
            context['all_friends'] = all_friends
            context['friends_row'] = friends_row
            context['count_friends'] = count_friends
            context['posts'] = posts
            return render(request, 'account/user_account.html', context=context)
        else:
            return redirect('login')
