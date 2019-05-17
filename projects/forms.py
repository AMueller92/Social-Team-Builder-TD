from django import forms
from django.forms.widgets import Textarea, TextInput

from accounts.models import Skill
from .models import Project, Position


class ProjectEditForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'duration',
            'requirements',
        ]
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter a project title'}
            ),
            'description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter a project description'}
            ),
            'requirements': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter project requirements'}
            ),
        }


class PositionEditForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Position
        fields = [
            'name',
            'length',
            'description',
            'skills',
        ]
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter a position title'}
            ),
            'description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter a description'}
            ),
        }


PositionFormSet = forms.modelformset_factory(Position,
                                             form=PositionEditForm,
                                             fields=('name', 'length', 'description', 'skills'),
                                             can_delete=True,
                                             min_num=1)
