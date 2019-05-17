from django import forms
from django.forms.widgets import Textarea, TextInput
from django.contrib.auth.models import User

from .models import Profile, Skill, SelfChoosenSkill, UserProject


class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username']


class ProfileEditForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Skill.objects.all()
    )

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


SkillFormSet = forms.modelformset_factory(SelfChoosenSkill,
                                          fields=('name',),
                                          extra=1,
                                          min_num=0)

UserProjectFormSet = forms.modelformset_factory(UserProject,
                                                fields=('title', 'url',),
                                                extra=1,
                                                min_num=0)
