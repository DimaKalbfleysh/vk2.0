from django import forms
from .models import Account, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введите текст"}),
        }