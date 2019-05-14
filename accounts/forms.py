from django import forms
from django.forms.widgets import Textarea, TextInput
from django.contrib.auth.models import User

from .models import Profile


class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username']


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'description',
            'image',
            'skills',
        ]
        widgets = {
            'description': Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Enter your description here'}
            ),
            'first_name': TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your first name here'}
            ),
            'last_name': TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your last name here'}
            ),
        }
