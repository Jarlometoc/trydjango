from django.forms import ModelForm
from .models import dbrerun
from django import forms   #for validation errors and hiddenfields

#ReRun form (allows for user to request a specific run number)

class ReRunForm(ModelForm):
    class Meta:
        model = dbrerun
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'runNum']  