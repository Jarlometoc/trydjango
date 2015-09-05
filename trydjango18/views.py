from django.shortcuts import render

def about(request):
    return render(request, 'about.html', {})   #from url newsletter.views.home