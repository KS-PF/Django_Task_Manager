from django import forms
from .models import TeamModels

class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamModels
        fields = ['name', 'description', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }