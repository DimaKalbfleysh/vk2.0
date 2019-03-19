from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'status', 'description', 'web_site']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'dark',
                                           'type': 'text',
                                           'id': 'pedit_first_name',
                                           'autocomplete': 'off',
                                           'spellcheck': "false"}),
            'status': forms.TextInput(attrs={'class': 'dark',
                                             'type': 'text',
                                             'id': 'pedit_last_name',
                                             'autocomplete': 'off',
                                             'spellcheck': "false"}),
            'description': forms.TextInput(attrs={'class': 'dark',
                                                  'type': 'text',
                                                  'id': 'pedit_last_name',
                                                  'autocomplete': 'off',
                                                  'spellcheck': "false"}),
            'web_site': forms.TextInput(attrs={'class': 'dark',
                                               'type': 'text',
                                               'id': 'pedit_last_name',
                                               'autocomplete': 'off',
                                               'spellcheck': "false"}),
        }
