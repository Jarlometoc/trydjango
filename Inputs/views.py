#Inputs
#******

#imports
#*******
from django.shortcuts import render
from .models import dbPDBdown, dbPDBup, dbEXPupload, dbPara, dbPara2
from Results.models import dbResults
from .forms import PDBdownForm, PDBupForm, EXPuploadForm, ParaForm, AddParaForm
from trydjango18.views import PathMaker, removePath
from Results.views import getLoadDict

#gather form data and place in the database
#******************************************

#pdb download
#************
def importPDBdown(request):

    #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
    rerun = getLoadDict(request.user.username)

    # maybe use UploadDataForm and have def to chunk: https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/
    if request.method == 'GET':
        PDBdown = PDBdownForm(initial={'username': request.user.username,'PDBdown': ''})

    else:
        PDBdown = PDBdownForm(request.POST, request.FILES)
        if PDBdown.is_valid():
            entry=dbPDBdown(username = request.POST.get('username'),
                        PDBdown = request.POST.get('PDBdown')
                        )
            entry.save()

        else:
            PDBdown = PDBdownForm(initial={'username': request.user.username,'PDBdown': ''})

    #update dbtoberun via the toberun function
    query = 'SELECT * FROM Inputs_dbpdbdown WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    object = dbPDBdown.objects.raw(query)[0]
    ToBeRunDict = toberun(object)

    return render(request, 'main.html',
              {'PDBdownHTML' : PDBdown,
               'ToBeRunHTML' : ToBeRunDict,
                'resultsHTML': rerun})   #include the dictionary of to be run key:value pairs


#pdb upload
#***********
def importPDBup(request):

    #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
    rerun = getLoadDict(request.user.username)

    # maybe use UploadDataForm and have def to chunk: https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/
    if request.method == 'GET':
        PDBup = PDBupForm(initial={'username': request.user.username,'PDBup': 'none chosen'})

    else:
        PDBup = PDBupForm(request.POST, request.FILES)
        if PDBup.is_valid():
            entry=dbPDBup(username = request.POST.get('username'),
                        PDBup = request.FILES['PDBup']
                        ) #obj containing files
            entry.save()
        else:
            PDBup = PDBupForm(initial={'username': request.user.username,'PDBup': 'none chosen'})


    #update dbtoberun via the toberun function
    query = 'SELECT * FROM Inputs_dbpdbup WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    object = dbPDBup.objects.raw(query)[0]
    ToBeRunDict = toberun(object)


    return render(request, 'main.html',
          {'PDBupHTML' : PDBup,
            'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': rerun})


#experimental LL data
#********************
def importEXP(request):

    #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
    rerun = getLoadDict(request.user.username)


    # maybe use UploadDataForm and have def to chunk: https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/
    if request.method == 'GET':
       EXP = EXPuploadForm(initial={'username': request.user.username,'EXPupload': 'none chosen'})

    else:
        EXP = EXPuploadForm(request.POST, request.FILES)
        if EXP.is_valid():
            entry=dbEXPupload(username = request.POST.get('username'),
                        EXPupload = request.FILES['EXPupload']
                        )                           #this is name of col in DB
            entry.save()
        else:
            EXP = EXPuploadForm(initial={'username': request.user.username,'EXPupload': 'none chosen'})

    #update newrundict.txt (to-be-run-parameters) via the toberun function
    query = 'SELECT * FROM Inputs_dbexpupload WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    object = dbEXPupload.objects.raw(query)[0]
    ToBeRunDict = toberun(object)

    return render(request, 'main.html',
          {'EXPHTML' : EXP,
            'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': rerun})

#parameters
#************
def importParameters(request):

    #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
    rerun = getLoadDict(request.user.username)

    if request.method == 'GET':
        Parameters = ParaForm(initial={'username': request.user.username, 'jobname': ' ', 'turns':5, 'units':27, 'rise':2.9, 'rescutL':0.0833333333, 'rescutH':0.3333333333, 'LorR':'R'})
    else:
        Parameters = ParaForm(request.POST)
        if Parameters.is_valid():
            entry=dbPara(username = request.POST.get('username'),
                        jobname = request.POST.get('jobname'),
                        turns = request.POST.get('turns'),
                        units = request.POST.get('units'),
                        rise = request.POST.get('rise'),
                        rescutL = request.POST.get('rescutL'),
                        rescutH = request.POST.get('rescutH'),
                        LorR = request.POST.get('LorR')
                        )
            entry.save()
        else:
           Parameters = ParaForm(initial={'username': request.user.username, 'jobname': ' ', 'turns':5, 'units':27, 'rise':2.9, 'rescutL':0.0833333333, 'rescutH':0.3333333333, 'LorR':'R'})

    #update newrundict.txt (to-be-run-parameters) via the toberun function
    query = 'SELECT * FROM Inputs_dbpara WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    object = dbPara.objects.raw(query)[0]
    ToBeRunDict = toberun(object)

    #RENDER
    return render(request, 'main.html',
              {'ParaHTML' : Parameters,
              'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': rerun})

#additional parameters
#*********************
def importPara2(request):

    #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
    rerun = getLoadDict(request.user.username)

    if request.method == 'GET':
        Parameters = AddParaForm(initial={'username': request.user.username, 'rfactor':'False', 'bfactor':20.0, 'bfactorSolv':400, 'bfactorSolvK':0.4, 'qfhtK1':2.0, 'qfhtK2':2.2, 'scscaling':0.92, 'gridR':256, 'gridZ':128, 'gridPhi':128})
    else:
        Parameters = AddParaForm(request.POST)
        if Parameters.is_valid():
            entry=dbPara2(username = request.POST.get('username'),
                        rfactor = request.POST.get('rfactor'),
                        bfactor = request.POST.get('bfactor'),
                        bfactorSolv = request.POST.get('bfactorSolv'),
                        bfactorSolvK = request.POST.get('bfactorSolvK'),
                        qfhtK1 = request.POST.get('qfhtK1'),
                        qfhtK2 = request.POST.get('qfhtK2'),
                        scscaling = request.POST.get('scscaling'),
                        gridR =request.POST.get('gridR'),
                        gridZ= request.POST.get('gridZ'),
                        gridPhi = request.POST.get('gridPhi')
                        )
            entry.save()
        else:
           Parameters = AddParaForm(initial={'username': request.user.username, 'rfactor':'False', 'bfactor':20.0, 'bfactorSolv':400, 'bfactorSolvK':0.4, 'qfhtK1':2.0, 'qfhtK2':2.2, 'scscaling':0.92, 'gridR':256, 'gridZ':128, 'gridPhi':128})

    #update newrundict.txt (to-be-run-parameters) via the toberun function
    query = 'SELECT * FROM Inputs_dbpara2 WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    object = dbPara2.objects.raw(query)[0]
    ToBeRunDict = toberun(object)

    #RENDER
    return render(request, 'main.html',
              {'AddHTML' : Parameters,
                'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': rerun})


#clear button; defaults all inputs
#*********************************
def Clear(request):
    #get -loaded- Results data, if any, for the Refresh, otherwise it will blank
    rerun = getLoadDict(request.user.username)
    if request.method == 'POST':   #if clear is pressed....
        #default all possible choices, save to appropriate db
        defDown = dbPDBdown(username=request.user.username, PDBdown='none chosen')
        defDown.save()
        defUp = dbPDBup(username=request.user.username, PDBup='none chosen')
        defUp.save()
        defEXP = dbEXPupload(username=request.user.username, EXPupload='none chosen')
        defEXP.save()
        defPara = dbPara(username=request.user.username, jobname=' ', turns=5, units=27, rise=2.9, rescutL=0.0833333333, rescutH=0.3333333333, LorR='R')
        defPara.save()
        defPara2 = dbPara2(username=request.user.username, bfactor=20.0, bfactorSolv=400, bfactorSolvK=0.4, gridPhi=128,
                           gridR=256, gridZ=128, qfhtK1=2.0, qfhtK2=2.2, rfactor='False', scscaling=0.92)
        defPara2.save()

        #now make a new newrundict.txt with default values
        newrundict(request.user.username)

        #retrieve the newrundict.txt to display 'to be run' files and parameters
        import json
        thefile = PathMaker(request.user.username, 'newrundict.txt')
        FHin = open(thefile, 'r')  #now open the new file
        #take out the dict
        defaultDict = json.load(FHin)
        FHin.close()
        #now run to default everything
        return render(request, 'main.html', {
            'ToBeRunHTML' : defaultDict, 'resultsHTML': rerun})



#Input-related functions
#***********************

#makes a to-be-run dictionary of parameters
def toberun(object):
    username = object.username  #need name for finding correct user dir
    #open newrundict.txt, open the dictionary
    import json
    thefile = PathMaker(username, 'newrundict.txt')
    try:
        FHin = open(thefile, 'r')
    except:
        newrundict(username) #if you cant open above, just make new file in user's dir and month with default settings
        FHin = open(thefile, 'r')  #now open the new file
    #take out the dict
    theDict = json.load(FHin)
    #open the object, take out whats needed
    #PDBdown
    if hasattr(object, 'PDBdown'):
        key = 'PDB'
        value= str(object.PDBdown)
        value = removePath(value)   #extra path removal bit, so just file name is seen
        theDict[key]=value
    #PDBup
    if hasattr(object, 'PDBup'):
        key = 'PDB'
        value= str(object.PDBup)
        value = removePath(value)   #extra path removal bit, so just file name is seen
        theDict[key]=value
    #Experimental
    if hasattr(object, 'EXPupload'):
        key = 'Optional_exp_layerlines'
        value= str(object.EXPupload)
        value = removePath(value)    #extra path removal bit, so just file name is seen
        theDict[key]=value
    #parameters
    if hasattr(object, 'jobname') and str(object.jobname) != ' ':
        key = 'jobname'
        value= str(object.jobname)
        theDict[key]=value
    if hasattr(object, 'turns'):
        key = 'turns'
        value= str(object.turns)
        theDict[key]=value
    if hasattr(object, 'units'):
        key = 'units'
        value= str(object.units)
        theDict[key]=value
    if hasattr(object, 'rise'):
        key = 'rise'
        value= str(object.rise)
        theDict[key]=value
    if hasattr(object, 'rescutH'):
        key = 'resolution (H)'
        value= str(object.rescutH)
        theDict[key]=value
    if hasattr(object, 'rescutL'):
        key = 'resolution (L)'
        value= str(object.rescutL)
        theDict[key]=value
    if hasattr(object, 'LorR'):
        key = 'handedness'
        value= str(object.LorR)
        theDict[key]=value
    #extra parameters (these should be added to dict only if not default vals)
    if hasattr(object, 'rfactor') and str(object.rfactor) != 'False':
        key = 'rfactor'
        value= str(object.rfactor)
        theDict[key]=value
    if hasattr(object, 'bfactor') and str(object.bfactor) != '20.0':
        key = 'bfactor'
        value= str(object.bfactor)
        theDict[key]=value
    if hasattr(object, 'bfactorSolv') and str(object.bfactorSolv) != '400.0':
        key = 'bfactorSolv'
        value= str(object.bfactorSolv)
        theDict[key]=value
    if hasattr(object, 'bfactorSolvK') and str(object.bfactorSolvK) != '0.4':
        key = 'bfactorSolvK'
        value= str(object.bfactorSolvK)
        theDict[key]=value
    if hasattr(object, 'qfhtK1') and str(object.qfhtK1) != '2.0':
        key = 'qfhtK1'
        value= str(object.qfhtK1)
        theDict[key]=value
    if hasattr(object, 'qfhtK2') and str(object.qfhtK2) != '2.2':
        key = 'qfhtK2'
        value= str(object.qfhtK2)
        theDict[key]=value
    if hasattr(object, 'scscaling') and str(object.scscaling) != '0.92':
        key = 'scscaling'
        value= str(object.scscaling)
        theDict[key]=value
    if hasattr(object, 'gridR') and str(object.gridR) != '256':
        key = 'gridR'
        value= str(object.gridR)
        theDict[key]=value
    if hasattr(object, 'gridZ') and str(object.gridZ) != '128':
        key = 'gridZ'
        value= str(object.gridZ)
        theDict[key]=value
    if hasattr(object, 'gridPhi') and str(object.gridPhi) != '128':
        key = 'gridPhi'
        value= str(object.gridPhi)
        theDict[key]=value
    #save the dict to the file and close
    fout = open(thefile, 'w')
    json.dump(theDict,fout)
    FHin.close()
    fout.close()
    #return saved dictionary
    return theDict


#resets the newrundict.txt to default: used by toberun() if newrundict.txt missing (first time or error)
def newrundict(username):   #need also for clear button 
    import json
    thefile = PathMaker(username, 'newrundict.txt')
    FHout = open(thefile, 'w')
    default= {'PDB': 'none chosen', 'Optional_exp_layerlines': 'none chosen', 'turns':5, 'units':27, 'rise':2.9, 'resolution (L)':0.0833333333, 'resolution (H)':0.3333333333, 'handedness':'R'}
    json.dump(default, FHout)
    FHout.close()
