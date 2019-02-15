import datetime
from django import forms
from account.models import Account
from django.forms import DateInput

from account.models import Photo


class EditUserForm(forms.ModelForm):
    date_of_birth = forms.CharField(label='Дата выписки',
                                    widget=forms.TextInput(attrs={'class': 'form-control col-2', 'type': 'date'}),
                                    required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'date_of_birth']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo']

        widgets = {
            'photo': forms.FileInput(attrs={'type': 'file'})
        }