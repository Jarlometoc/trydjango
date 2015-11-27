#View Results of any run; default is most-recent run
#***************************************************

#imports
#********
from .forms import ReRunForm
from django.shortcuts import render
from Results.models import dbResults
from trydjango18.views import PathMaker, removePath
import json
import shutil
from trydjango18.views import Sound
import urllib.request

#Retrieve data from a run
#*************************

def LoadRun(request):  # when Load is entered.....

    #include ToBeRun dictionary from inputs, so they dont disappear during page refresh
    ToBeRunDict = getRunDict(request.user.username)

    #Make Results object for printing to main:  MOST RECENT ENTRY!
    query = 'SELECT * FROM Results_dbresults WHERE username = "' + request.user.username + '" ORDER BY id DESC LIMIT 1'
    Qobject6 = dbResults.objects.raw(query)[0]
    toreturn = UsedParam(Qobject6)

    #move current layerlines.png to static for rendering
    source = str(Qobject6.LLoutputPic)
    #Django want pic in both our_static and root_static...
    shutil.copyfile(source, 'static_in_pro/static_root/images/UserLL.png')
    shutil.copyfile(source, 'static_in_pro/our_static/images/UserLL.png')

    #jmol display
    #************
    #use fibrilPDB, returns LLoutputPic
    try:
        UseJmol(Qobject6.fibrilPDB)  #path to the fibrilPDB made by Rosetta
    except:
        Sound(4)


    #RENDER
    return render(request, 'main.html', {'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': toreturn})



#Rerun button: User enters previous run number (if none, defaults to regular run)
def ReRun(request):

    #include ToBeRun dictionary from inputs
    ToBeRunDict = getRunDict(request.user.username)

    if request.method == 'GET':
        rerunF = ReRunForm(initial={'runNum': '1'})
    else:
        rerunF = ReRunForm(request.POST)
        if rerunF.is_valid():
            runNum = request.POST.get('runNum')   # or runNum = rerunF.cleaned_data['runNum']
            # use the most-recent-run-number to pull up that row in the results db
            query2 = 'SELECT * FROM Results_dbresults WHERE username = "' + request.user.username + '" AND id =' + \
                     str(runNum)
            Qobject6 = dbResults.objects.raw(query2)[0]
            toreturn = UsedParam(Qobject6)

            #move current layerlines.png to static for rendering
            source = str(Qobject6.LLoutputPic)
            shutil.copyfile(source, 'static_in_pro/static_root/images/UserLL.png')
            shutil.copyfile(source, 'static_in_pro/our_static/images/UserLL.png')

            #insert Jmol code from above


            #RENDER
            return render(request, 'main.html', {'resultsHTML': toreturn, 'ToBeRunHTML' : ToBeRunDict})
        else:
            #empty, but need to include input data
            rerunF = ReRunForm(initial={'runNum': '1'})
            return render(request, 'main.html', {'ReRunHTML': rerunF, 'ToBeRunHTML' : ToBeRunDict})

    #empty, but need to include input data
    return render(request, 'main.html', {'ReRunHTML': rerunF, 'ToBeRunHTML' : ToBeRunDict})


#Sends results to user's email
#*****************************
def EmailResults(request):
    if request.method == 'POST':  # when send results button pushed....
        from django.conf import settings
        from django.core.mail.message import EmailMessage
        from django.contrib.auth.models import User
        # get user email from auth_user db
        query = 'SELECT * FROM auth_user WHERE username = "' + request.user.username + '" ORDER BY id DESC LIMIT 1'
        Qobject8 = User.objects.raw(query)[0]  # db called User in Django, auth_user in SQL
        userEmail = str(Qobject8.email)
        # get user run info
        query2 = 'SELECT * FROM Results_dbresults WHERE username = "' + request.user.username + '" ORDER BY id DESC LIMIT 1'
        Qobject6 = dbResults.objects.raw(query2)[0]
        bodytext = 'Here are your requested results for Run Number ' + str(Qobject6.id) + ' carried out on ' + str(
            Qobject6.timestamp)
        emailResults = EmailMessage(subject='Results of FAT analysis',
                                    body=bodytext,
                                    from_email=settings.EMAIL_HOST_USER,
                                    to=[userEmail]
                                    )
        #make the zipfile
        Path = ZipIt(request, Qobject6)
        # attach results.zip
        emailResults.attach_file(Path)  # attach the zip file
        emailResults.send()  # need to .send()

        #also include ToBeRun dictionary from inputs
        ToBeRunDict = getRunDict(Qobject6.username)

        #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
        rerun = getLoadDict(request.user.username)

        #RENDER
        return render(request, 'main.html',{'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': rerun})


#Downloads user's results  !!!!make sure it picks what's on screen and not auto most recent!!!
#************************
def DownloadResults(request):
    if request.method == 'POST':  # if download is pressed.....
        # zip Jmol, LL, chisq (score.sc) to email and download
        import os, zipfile
        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper
        # get most recent zip of results
        query = 'SELECT * FROM Results_dbresults WHERE username = "' + request.user.username + '" ORDER BY id DESC LIMIT 1'
        Qobject6 = dbResults.objects.raw(query)[0]
        # make the zipfile
        file = ZipIt(request, Qobject6)
        # code for downloading a file
        wrapper = FileWrapper(open(file, 'rb'))  # 'rb' is windows fix
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(file)  # loads in chunks: see FileWrapper
        return response


#Results-related functions
#*************************

# Make UsedParameters a .txt file for downloading
def ParamUsedFile(Qobject6, used):
    Path = PathMaker(Qobject6.username, 'parameters.txt')
    FH = open(Path, 'w')
    FH.write('Files and Parameters used for FAT Run Number ' + str(Qobject6.id))
    FH.write("\n")
    FH.write('User' + ": " + str(Qobject6.username) + "\n")
    FH.write('Date' + ": " + used['Run date'] + "\n")
    try:
        FH.write('jobname' + ": " + used['jobname'] + "\n")
    except:
        pass
    FH.write("\n\n")
    FH.write("Files:\n")
    FH.write("\t" + 'PDB'  + ": "+ used['PDB']+"\n")
    FH.write("\t"+ 'Optional exp. layerlines' + ": " + used['Optional_exp_layerlines']+ "\n")
    FH.write("\n\n")
    FH.write("Parameters:\n")
    for key in used:
        if (key == 'ID' or key == 'Run date' or key == 'jobname' or key == 'PDB' or key == 'Optional_exp_layerlines'):
            next
        else:
            FH.write("\t"+ key + ": " + used[key])
            FH.write("\n")
    FH.close()


#Zipping files for sending
def ZipIt(request, Qobject6):
    import zipfile
    # remove old
    import os
    try:
        pathtoold = PathMaker(request.user.username, 'results.zip')
        os.remove(pathtoold)
    except OSError:
        pass
    from Results.models import dbResults
    # Make Results object
    # query = 'SELECT * FROM Inputs_dbresults WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    # Qobject6 = dbResults.objects.raw(query)[0]

    # select table columns to send; fibril.pdb, LayerLines.jpg and parameters.txt
    fibfile = str(Qobject6.fibrilPDB)
    LLout = str(Qobject6.LLoutputPic)
    parampath = PathMaker(request.user.username, 'parameters.txt')
    # give file a name and location in user's dir
    filename = 'results.zip'
    Path = PathMaker(request.user.username, filename)
    # remove paths
    from os.path import basename
    # buffer = StringIO()
    zipped = zipfile.ZipFile(Path, 'w')
    zipped.write(fibfile, basename(fibfile))
    zipped.write(LLout, basename(LLout))
    zipped.write(parampath, basename(parampath))
    zipped.close()
    return Path


#Results for a given run:
def UsedParam(Qobject6):  #inputed object containing the chosen run number
    used = {'ID': str(Qobject6.id),
            'Run date':  str(Qobject6.timestamp),
            'PDB':  removePath(str(Qobject6.PDBused)),
            'Optional_exp_layerlines': removePath(str(Qobject6.experimentalData)),
            'Turns':  str(Qobject6.turns),
            'Units' : str(Qobject6.units),
            'Rise' : str(Qobject6.rise),
            'Resolution (L)': str(Qobject6.rescutL),
            'Resolution (H)' : str(Qobject6.rescutH),
            'Handedness':  str(Qobject6.LorR)}
    if Qobject6.jobname != ' ':
        used['jobname'] = str(Qobject6.jobname)
    if Qobject6.bfactor != 20.0:
        used['Bfactor'] =  str(Qobject6.bfactor)
    if Qobject6.bfactorSolv != 400:
        used['BfactorSolv'] = str(Qobject6.bfactorSolv)
    if Qobject6.bfactorSolvK != 0.4:
        used['BfactorSolvK'] = str(Qobject6.bfactorSolvK)
    if Qobject6.qfhtK1 != 2.0:
        used['qfhtK1'] =  str(Qobject6.qfhtK1)
    if Qobject6.qfhtK2 != 2.2:
        used['qfhtK2'] =  str(Qobject6.qfhtK2)
    if Qobject6.scscaling != 0.92:
        used['sc_scaling'] = str(Qobject6.scscaling)
    if Qobject6.gridR != 256:
        used['gridR'] =  str(Qobject6.gridR)
    if Qobject6.gridZ != 128:
        used['gridZ'] =  str(Qobject6.gridZ)
    if Qobject6.gridPhi != 128:
        used['gridPhi'] =  str(Qobject6.gridPhi)
    if Qobject6.experimentalData != 'none chosen':
        used['Chi-square'] =  str(Qobject6.chisq)

    #make parameters.txt for email/download
    ParamUsedFile(Qobject6, used)

    #make 'CurrentLoaded.txt' with the 'used' dictionary so data can be displayed in other renders
    thefile = PathMaker(Qobject6.username, 'CurrentLoaded.txt')
    fout = open(thefile, 'w')
    json.dump(used, fout)
    fout.close()


    #Logic for displaying fibrilarPDB using Jmol and LLimage
   # used['forJmol'] = str(Qobject6.fibrilPDB)        #this is the -input- for Jmol
   # if Qobject6.experimentalData != 'none chosen':
       # used['forLLpic'] = str(Qobject6.LLoutputPic)   #this is the -output- of LayerLinesToImage.py


    #include most recent newrundict.txt, so it can be displayed during page refresh
    rundict=getRunDict(Qobject6.username)
    used['ToBeRunHTML'] = rundict

    #for display on mainpage
    return used


#gets the most recent newrundict.txt, so it can be displayed during any page refresh of main.html
def getRunDict(username):
    thefile = PathMaker(username, 'newrundict.txt')
    FHin = open(thefile, 'r')
    #take out the dict
    theDict = json.load(FHin)
    return theDict

#gets the most current loaded results in dict form
def getLoadDict(username):
    thefile = PathMaker(username, 'CurrentLoaded.txt')
    try:
        FHin = open(thefile, 'r')
        #take out the dict
        DictLoadedResults = json.load(FHin)
        FHin.close()
    except:
        DictLoadedResults = {}
    return DictLoadedResults

#UseJmol takes fibrilPDB output from Rosetta, hands it to Jmol for display
def UseJmol(fibrilPDB):
    pass
