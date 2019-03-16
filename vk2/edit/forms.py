import datetime
from django import forms
from account.models import Account
from django.forms import DateInput

from account.models import Photo


class EditUserForm(forms.ModelForm):
    date_of_birth = forms.CharField(label='Дата рождения',
                                    widget=forms.TextInput(attrs={'class': 'form-control col-2', 'type': 'date'}),
                                    required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'date_of_birth', 'sex', 'marital_status', 'birth_day', 'month_birth',
                  'year_birth', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'dark',
                                                 'type': 'text',
                                                 'id': 'pedit_first_name',
                                                 'autocomplete': 'off',
                                                 'spellcheck': "false"}),
            'last_name': forms.TextInput(attrs={'class': 'dark',
                                                'type': 'text',
                                                'id': 'pedit_last_name',
                                                'autocomplete': 'off',
                                                'spellcheck': "false"}),
            'email': forms.TextInput(attrs={'class': 'dark',
                                            'type': 'text',
                                            'id': 'pedit_last_name',
                                            'autocomplete': 'off',
                                            'spellcheck': "false"}),
            'sex': forms.Select(attrs={'class': 'dark'}),
            'marital_status': forms.Select(attrs={'class': 'dark'}),
            'birth_day': forms.Select(attrs={'class': 'dark day'}),
            'month_birth': forms.Select(attrs={'class': 'dark month'}),
            'year_birth': forms.Select(attrs={'class': 'dark day'})
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo']

        widgets = {
            'photo': forms.FileInput(attrs={'type': 'file'})
        }
