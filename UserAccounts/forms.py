#for contact us!
from django import forms
class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()




#from django import forms
#from .models import SignUp
#class SignUpForm(forms.ModelForm):
    #class Meta:
        #model = SignUp
        #fields = ['full_name', 'email']