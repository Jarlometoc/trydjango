# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import dbPDBdown, dbPDBup, dbEXPupload, dbPara, dbPara2
from django import forms   #for validation errors and hiddenfields

#Forms
#******

#download from RCSB
class PDBdownForm(ModelForm):
    class Meta:
        model = dbPDBdown
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'PDBdown']  #to select all subset from this db


#upload local file
class PDBupForm(ModelForm):
    class Meta:
        model = dbPDBup
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'PDBup']


#upload experimental LL data
class EXPuploadForm(ModelForm):
    class Meta:
        model = dbEXPupload
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'EXPupload']


#parameters
class ParaForm(ModelForm):
    class Meta:
        model = dbPara
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'jobname', 'turns', 'units', 'rise', 'rescutL', 'rescutH', 'LorR']


#additional parameters
class AddParaForm(ModelForm):
    class Meta:
        model = dbPara2
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'rfactor', 'bfactor', 'bfactorSolv', 'bfactorSolvK', 'qfhtK1',
                    'qfhtK2', 'scscaling', 'gridR', 'gridZ', 'gridPhi']


