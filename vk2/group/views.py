from django.shortcuts import render, redirect
from django.views import View
from account.models import Account
from group.models import Group
from group.forms import GroupForm


class GroupsView(View):
    def get(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        groups = main_user.group.all()
        groups_under_management = groups.filter(admin=main_user)
        return render(request, 'group/groups.html', context={'main_user': main_user,
                                                             'groups': groups,
                                                             'groups_under_management': groups_under_management})


class GroupView(View):
    def get(self, request, pk):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        group = Group.objects.select_related().get(pk=pk)
        posts = group.posts.select_related()
        return render(request, 'group/public.html', context={'main_user': main_user,
                                                             'group': group,
                                                             'posts': posts})


class GroupCreateView(View):
    def get(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        form = GroupForm
        return render(request, 'group/create.html', context={'main_user': main_user,
                                                             'form': form})

    def post(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        group = Group.objects.create()
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group.admin.add(main_user)
            group.subscribers.add(main_user)
            form.save()
            group.save()
        return redirect('group', pk=group.pk)


class GroupEditView(View):
    def get(self, request, pk):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        group = Group.objects.select_related().get(pk=pk)
        form = GroupForm(instance=group)
        return render(request, 'group/edit.html', context={'main_user': main_user,
                                                           'group': group,
                                                           'form': form})

    def post(self, request, pk):
        group = Group.objects.select_related().get(pk=pk)
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
        return redirect('group', pk=group.pk)


class SubscribeToGroup(View):
    def get(self, request, pk):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        group = Group.objects.select_related().get(pk=pk)
        group.subscribers.add(main_user)
        group.save()
        return redirect('group', pk=group.pk)