from django.shortcuts import render
from .forms import ContactForm  #for contact form additon
from .forms import SignUpForm

#For email
#*************************
from django.conf import settings  #pick and choose from settings
from django.core.mail import send_mail  #see django example
#**************************

def home(request):
    title = 'New and Returning'
    #if request.user.is_authenticated():
     #   title = "Welcome Back %s"  %(request.user)

    form = SignUpForm()
    context = {
        "title": title,    #context dict
        "form": form
    }
    return render(request, 'home.html', context)   #from url UserAccounts.views.home

#Email us!
#*********
#function for ContactForm (provides all info needed for 'Contact us'
def contact(request):
    title = 'Contact us'
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")

        #for email from user to us
        #*********************
        subject = 'FAT contact form'
        from_email = settings.EMAIL_HOST_USER #from settings.py, so need import
        to_email = [from_email]  #list so you can do many
        contact_message = "%s wrote: %s, using the email: %s" %(form_full_name, form_message, form_email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently = False)
        #**********************

    #present the form on the contact us page
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "forms.html", context)