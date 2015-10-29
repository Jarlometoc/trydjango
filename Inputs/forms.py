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

    #functions (methods) clean the data
    def clean_PDBdown(self):
        PDBdown = self.cleaned_data.get('PDBdown') #the actual file
        #if ".pdb" not in PDB:
            #raise forms.ValidationError("Use a .dat file")
        return PDBdown

#upload local file
class PDBupForm(ModelForm):
    class Meta:
        model = dbPDBup
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'PDBup']


   # def clean_PDBup(self):
       # PDBup = self.cleaned_data.get('PDBup') #the actual file
        #if ".pdb" not in PDB:
            #raise forms.ValidationError("Use a .dat file")
       # return PDBup

#upload experimental LL data
class EXPuploadForm(ModelForm):
    class Meta:
        model = dbEXPupload
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'EXPupload']

   # def clean_EXPupload(self):
      # EXPupload = self.cleaned_data.get('EXPupload') #the actual file
        #if ".dat" not in EXPupload:
            #raise forms.ValidationError("Use a .dat file")
       # return EXPupload

#parameters
class ParaForm(ModelForm):
    class Meta:
        model = dbPara
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'turns', 'units', 'rise', 'rescutL', 'rescutH', 'LorR']

    def clean_turns(self):
        turns = self.cleaned_data.get('turns')
        if turns != 5:
            raise forms.ValidationError("Turns need to be equal to 5")
        return turns

    def clean_units(self):
        units = self.cleaned_data.get('units')
        if units == 0:
            raise forms.ValidationError("Units need to be more than 0")
        return units

    def clean_rise(self):
        rise = self.cleaned_data.get('rise')
        if rise == 0 :
            raise forms.ValidationError("Rise need to be more than 0")
        return rise

    #def clean_LorR(self):
       #LorR = self.cleaned_data.get('LorR')
      # if LorR != 'L' or LorR != 'R' or LorR != 'l' or LorR != 'r':
          #raise forms.ValidationError("Enter L or R")
      # return LorR

#additional parameters
class AddParaForm(ModelForm):
    class Meta:
        model = dbPara2
        widgets = {'username': forms.HiddenInput()}
        fields =['username', 'rfactor', 'bfactor', 'bfactorSolv', 'bfactorSolvK', 'qfhtK1',
                    'qfhtK2', 'scscaling', 'gridR', 'gridZ', 'gridPhi']

#ReRun form (allows for user to request a specific run number
class ReRunForm(forms.Form):
    runNum = forms.CharField(max_length=4)

