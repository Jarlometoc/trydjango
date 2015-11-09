from django import forms

#ReRun form (allows for user to request a specific run number: need a (form to accept data from the input box)
#but no corresponding model (table in db)

class ReRunForm(forms.Form):
    runNum = forms.CharField(max_length=4)
