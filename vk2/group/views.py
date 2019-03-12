from django.shortcuts import render
from django.views import View

from account.models import Account, Group


class GroupsView(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        groups = Group.objects.all()
        return render(request, 'group/groups.html', context={'main_user': main_user, 'groups': groups})


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
        return render(request, 'group/public.html', context={'main_user': main_user,
                                                             'group': group,
                                                             'posts': posts,
                                                             'fixed_post': fixed_post})
