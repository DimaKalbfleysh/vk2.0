from django.shortcuts import render, redirect
from django.views import View
from edit.forms import EditUserForm, PhotoForm
from account.models import Account
from group.models import Group


class EditUser(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        form = EditUserForm(instance=main_user)
        return render(request, 'edit/edit_user.html', context={'main_user': main_user,
                                                               'form': form})

    def post(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        form = EditUserForm(request.POST, instance=main_user)
        if form.is_valid():
            form.save()
        return redirect('account', pk=main_user.pk)
