from django import forms

from account.models import Account
from django.contrib.auth.forms import AuthenticationForm

# 'placeholder': "Телефон или email"


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Телефон или email"}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Пароль"}),
        }