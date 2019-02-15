from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from register.forms import InitRegisterUserForm
from register.forms import FinalRegisterUserForm

from account.models import Account


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
        form = FinalRegisterUserForm
        return render(request, 'register/final_register_user.html', context={'form': form,
                                                                             'usnm': username})

    def post(self, request, username):
        user = Account.objects.get(username=username    )
        form = FinalRegisterUserForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
            except:
                user.date_of_birth = None
                form.save()
        authenticate(username=username, password=user.password)
        login(request, user)
        return redirect('account', pk=request.user.pk)