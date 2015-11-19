#Webpages
#********

#imports
import datetime
from django.shortcuts import render
import os


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
    #here you check if that name/Month dir exists, if not, create
    if not os.path.exists('static_in_pro/media_root/Storage/'+ name + "/" + Month):
        os.makedirs('static_in_pro/media_root/Storage/'+ name + "/" + Month)
    #now return path to file
    return '/'.join(['static_in_pro/media_root/Storage', name, Month, filename])  #need 'static_in_pro/media_root'

#Pathmaker specific for upload= function of models
def PathMaker2(request, filename):
    name = request.username
    TodaysDate = datetime.date.today()
    Month = str(TodaysDate.month)
    #here you check if that name/Month dir exists, if not, create
    if not os.path.exists('static_in_pro/media_root/Storage/'+ name + "/" + Month):
        os.makedirs('static_in_pro/media_root/Storage/'+ name + "/" + Month)
    #now return path to file
    return '/'.join(['Storage', name, Month, filename])  #need 'static_in_pro/media_root'



#Remove paths from files for the zipped results
def removePath(path):
    import ntpath
    trimmed = ntpath.basename(path)  #careful: does not deal with 'file.txt/' syntax
    return trimmed

#sound for debugging
def Sound(i):  #beep number as argument
    while i>0:
        import winsound
        Freq = 2000 # Set Frequency To 2500 Hertz
        Dur = 100 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur)
        i -= 1