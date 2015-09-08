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

def contact(request):
    title = 'Contact us'
    form = ContactForm(request.POST or None)

    #for email
    #*********************
    subject = 'Site contact form'
    from_email = settings.EMAIL_HOST_USER #from settings.py, so need import
    to_email = [from_email]  #list so you can do many
    contact_message = "test"  #or: = " %s, %s via %s" %(full_name, message, email), but need to import this somehow
    send_mail(subject, contact_message, from_email, to_email, fail_silently = False)
    #**********************

    context = {
        "form": form,
        "title": title,
    }
    return render(request, "forms.html", context)