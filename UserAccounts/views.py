from django.shortcuts import render
from .contactform import ContactForm


#For email
#*************************
from django.conf import settings
from django.core.mail import send_mail
#**************************

#Email us!
#*********
#function for ContactForm (provides all info needed for 'Contact us')
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

        #Return to landing after sending email
        return render(request, 'home.html', {})

    #present the form on the contact us page
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "contact.html", context)
