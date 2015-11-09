#Webpages
#********

#imports
import datetime
from django.shortcuts import render

#page views
def home(request):
  return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def main(request):
    if request.user.is_authenticated():
        return render(request, 'main.html', {})   #mainpage with rosetta: only access if logged in
    else:
        return render(request, 'home.html', {})



#generic functions
#*****************

#Takes username and file, returns a path to user's Storage file (by month)
def PathMaker(name, filename):
    TodaysDate = datetime.date.today()
    Month = str(TodaysDate.month)
    return '/'.join(['static_in_pro/media_root/Storage', name, Month, filename])  #need 'static_in_pro/media_root'

#Remove paths from files for the zipped results
def removePath(path):
    import ntpath
    trimmed = ntpath.basename(path)  #careful: does not deal with 'file.txt/' syntax
    return trimmed
