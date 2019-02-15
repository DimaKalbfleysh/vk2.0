from django import forms
from account.models import Account


class InitRegisterUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Телефон или email"}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Пароль"}),
        }


class FinalRegisterUserForm(forms.ModelForm):
    date_of_birth = forms.CharField(label='Дата рождения',
                                    widget=forms.TextInput(attrs={'class': 'form-control col-2', 'type': 'date'}),
                                    required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'date_of_birth']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Имя"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Фамилия"}),
        }
