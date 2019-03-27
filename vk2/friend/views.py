from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from account.models import Account
from friend.models import FriendshipRequest
from friend.models import Friend


class FriendsView(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        f = Friend.objects.get(who=user)
        all_friends = f.users.all()
        user.number_friends = all_friends.count()
        user.save()
        context = dict()
        context['user'] = user
        context['main_user'] = main_user
        context['all_friends'] = all_friends
        return render(request, 'friend/friends.html', context=context)


class FriendsAllRequest(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        unrejected_requests = main_user.friendship_to_user.filter(is_accept=False)
        main_user.unrejected_request_number = unrejected_requests.count()
        main_user.save()
        context = dict()
        context['user'] = user
        context['main_user'] = main_user
        context['unrejected_requests'] = unrejected_requests
        return render(request, 'friend/all_request.html', context=context)


class FriendsAllUsers(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        user = Account.objects.get(pk=pk)
        all_users = Account.objects.all()
        context = dict()
        context['user'] = user
        context['main_user'] = main_user
        context['all_users'] = all_users
        return render(request, 'friend/all_users.html', context=context)


class UpdateFriendshipRequest(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        unrejected_requests = main_user.friendship_to_user.filter(is_accept=False)
        main_user.unrejected_request_number = unrejected_requests.count()
        main_user.save()
        context = dict()
        context['unrejected_requests'] = unrejected_requests.count()
        return JsonResponse(context)


class Request(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        to_user = Account.objects.get(pk=pk)
        FriendshipRequest.objects.create(from_user=main_user, to_user=to_user)
        return redirect('account', pk=pk)


class Accept(View):
    def get(self, request, pk):
        main_user = Account.objects.get(pk=request.user.pk)
        from_user = Account.objects.get(pk=pk)
        frendship_request = FriendshipRequest.objects.get(from_user=from_user, to_user=main_user)
        frendship_request.is_accept = True
        frendship_request.save()
        f = Friend.objects.get(who=main_user)
        q = Friend.objects.get(who=from_user)
        f.users.add(from_user)
        q.users.add(main_user)
        return redirect('account', pk=pk)