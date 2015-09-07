from django.shortcuts import render

def about(request):
    return render(request, 'about.html', {})   #from url newsletter.views.home

def main(request):
    if request.user.is_authenticated():
        return render(request, 'main.html', {})   #mainpage
    else:
        return render(request, 'home.html', {})