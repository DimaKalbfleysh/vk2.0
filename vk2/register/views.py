from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from register.forms import InitRegisterUserForm
from register.forms import FinalRegisterUserForm
from account.models import Account
from edit.forms import EditUserForm


class InitRegisterUser(View):
    def get(self, request):
        form = InitRegisterUserForm
        return render(request, 'register/init_register_user.html', context={'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = Account.objects.create_user(username=username, password=password)
        return redirect('final_register', username=user.username)


class FinalRegisterUser(View):
    def get(self, request, username):
        form = EditUserForm
        return render(request, 'register/final_register_user.html', context={'form': form,
                                                                             'usnm': username})

    def post(self, request, username):
        user = Account.objects.get(username=username)
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        authenticate(username=username, password=user.password)
        login(request, user)
        return render(request, 'register/verify.html', context={'form': form,
                                                                             'usnm': username})


class Verify(View):
    def get(self, request, pk):
        try:
            user = Account.objects.get(pk=pk, is_verified=False)
        except Account.DoesNotExist:
            raise Http404("User does not exist or is already verified")

        user.is_verified = True
        user.save()
        return redirect('account', pk=user.pk)