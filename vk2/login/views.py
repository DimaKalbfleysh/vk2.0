from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from login.forms import LoginUserForm
from register.forms import InitRegisterUserForm


class LoginUser(View):
    def get(self, request):
        form = LoginUserForm
        register_form = InitRegisterUserForm
        return render(request, 'login/login_user.html', context={'form': form,
                                                                 'register_form': register_form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('account', pk=user.pk)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')
