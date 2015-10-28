#main views to load the various pages
from django.shortcuts import render, HttpResponse
from django.core.mail import EmailMessage
def home(request):
  return render(request, 'home.html', {}) #context)

def about(request):
    return render(request, 'about.html', {})

def main(request):
    if request.user.is_authenticated():
        return render(request, 'main.html', {})   #mainpage
    else:
        return render(request, 'home.html', {})


#Collect data from various databases, run denovo, Rosetta, LayerLinesToImage and save results to results DB
#**********************************************************************************************************
import datetime
from Inputs.models import dbPDBdown, dbPDBup, dbEXPupload, dbFlag, dbPara, dbResults, dbPara2, dbReRun
from Inputs.forms import ReRunForm
import subprocess


#Main function
#*************
def Testing(request, auto=0):
    if request.method == 'POST' or auto == 1:   #if Run is pressed....

        #SQL to make query objects for each table
        #****************************************
        #download
        query = 'SELECT * FROM Inputs_dbpdbdown WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject = dbPDBdown.objects.raw(query)[0]

        #upload
        query = 'SELECT * FROM Inputs_dbpdbup WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject2 = dbPDBup.objects.raw(query)[0]

        #Experimental
        query = 'SELECT * FROM Inputs_dbexpupload WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject3 = dbEXPupload.objects.raw(query)[0]

        #Parameters
        query = 'SELECT * FROM Inputs_dbpara WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject4 = dbPara.objects.raw(query)[0]

        #Additional Parameters
        query = 'SELECT * FROM Inputs_dbpara2 WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject4B = dbPara2.objects.raw(query)[0]

        #Identify the most current upload or download by timestamp, choose most recent
        if Qobject.timestamp > Qobject2.timestamp:
            chosenPDB = fetch_pdb(Qobject)

        else:
            chosenPDB = Qobject2.PDBup


        #Make FlagsFile using the query objects
        #**************************************
        #place into variables
        PDB = '-in:file:s '+ str(chosenPDB)   #the chosen PDB, based on most recent timestamp
        EXP =  '-fiber_diffraction:layer_lines '+ str(Qobject3.EXPupload)     #File containing fiber diffraction layer lines
        Units = '-fiber_diffraction:a '+ str(Qobject4.units)     #number of units
        Turns = '-fiber_diffraction:b '+ str(Qobject4.turns)    #number of turns
        Rise = '-fiber_diffraction:p '+ str(Qobject4.rise)     #If specified, subunit rise is taken from input, otherwise is calculated by the program
        Lcutoff = '-fiber_diffraction:resolution_cutoff_low '+ str(Qobject4.rescutL)  #Resolution cutoff 12Å
        Hcutoff = '-fiber_diffraction:resolution_cutoff_high '+ str(Qobject4.rescutH)  #Resolution cutoff 3Å
        LorR = '-fiber_diffraction:LorR '+ str(Qobject4.LorR)   #Left or Right handed
       #Additional Parameters
        Rfac = '-fiber_diffraction:rfactor_refinement '+ str(Qobject4B.rfactor)    #If set R factor instead of chi2 is used in scoring and derivatives calculations
        AtomicBF = '-fiber_diffraction::b_factor '+ str(Qobject4B.bfactor)    #Atomic B-factor
        Solv = '-fiber_diffraction::b_factor_solv '+ str(Qobject4B.bfactorSolv)   #temperature factor that accounts for the disordered solvent
        SolvK = '-fiber_diffraction::b_factor_solv_K '+ str(Qobject4B.bfactorSolvK)   #scale factor that adjust average solvent scattering intensity
        K1 = '-fiber_diffraction:qfht_K1 '+ str(Qobject4B.qfhtK1)    #Hankel transform K1 parameter
        K2 = '-fiber_diffraction:qfht_K2 '+ str(Qobject4B.qfhtK2)      #Hankel transform K1 parameter
        SC = '-edensity:sc_scaling '+ str(Qobject4B.scscaling)    #Hankel transform K1 parameter
        GridR = '-fiber_diffraction:grid_r '+ str(Qobject4B.gridR)     #Grid size r, should be bigger than radius of molecule
        GridZ = '-fiber_diffraction:grid_z '+ str(Qobject4B.gridZ)     #Grid size z, should be bigger than molecule span in z direction
        GridPhi = '-fiber_diffraction:grid_phi '+ str(Qobject4B.gridPhi)    #Grid size phi, change if higher accuracy is needed
        #output for Rosetta
        fibPDBout = '-out:file ' + PathMaker(Qobject.username, 'fibril.pdb')
        LLout = '-fiber_diffraction:output_fiber_spectra ' + PathMaker(Qobject.username, 'intensity.txt')   #to make LLpic, stored in user's folder'
        Score = '-out:file:scorefile ' + PathMaker(Qobject.username, 'score.sc')
        scoreWeights = '-score:weights Storage/fiberdiff.txt'  #unused output, ignore

        #make a list of the above variables
        ParameterList = [PDB,
                         EXP,
                         Units,
                         Turns,
                         Rise,
                         Lcutoff,
                         Hcutoff,
                         LorR,
                         Rfac,
                         AtomicBF,
                         Solv,
                         SolvK,
                         K1,
                         K2,
                         SC,
                         GridR,
                         GridZ,
                         GridPhi,
                         fibPDBout,
                         LLout,
                         Score,
                         scoreWeights]

        #make the Flags file, tagged with username, placed in user's folder
        filename = Qobject.username + '_Flags'
        Path = PathMaker(Qobject.username, filename)
        FHout = open(Path, 'w')
        for item in ParameterList:
            FHout.write("%s\n" % item)
        FHout.close()
        #now save path to dbFlags
        addFlag = dbFlag(username=Qobject.username, FlagFile=Path)
        addFlag.save()


        #Path variables for dbResults  **make sure their -creation- also points to same
        denovoPath = str(PathMaker(Qobject.username, 'helix_denovo.sdef'))
        fibrilPDBPath = str(PathMaker(Qobject.username, 'fibril.pdb'))
        scorePath = str(PathMaker(Qobject.username, 'score.sc'))
        intensityPath = str(PathMaker(Qobject.username, 'intensity.txt'))
        LLpicPath = str(PathMaker(Qobject.username, 'layerlines.jpg'))


        #Run make_helix_denovo
        #*********************
        #input units/rise/turns/N=40, plus optional files, returns helix_denovo.sdef- symmetry info for Rosetta

        try:
            #make commandline and run  eg, './make_helix_denovo.py -p 2.9 -n 40 -v 5 -u 27 –c L'
            command = './make_helix_denovo.py' + \
                      ' -p ' + str(Qobject4.rise) + \
                      ' -u ' + str(Qobject4.units) + \
                      ' -n 40' + \
                      ' -v ' + str(Qobject4.turns) + \
                      ' -c ' + str(Qobject4.LorR) + \
                      ' -o ' + denovoPath + \
                      ' -r Storage/virtual_residues_file'
                      #-o is output of helix_denovo.sdef
                      #virtual_residues_file also made each run: for diagnostics

            subprocess.call(command, shell=True)

        except:  #subprocess.CalledProcessError:    !causes error if added!
            pass


        #modifying grit.dat here prior to use with Rosetta


        #run Rosetta
        #***********
        #qQuery dbFlag and make an object containing everything
        query = 'SELECT * FROM Inputs_dbflag WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject5 = dbFlag.objects.raw(query)[0]

        #'./score.linuxgccrelease @FlagFilePath'
        try:
            command = './score.linuxgccrelease ' + \
                      '@' + str(Qobject5.FlagFile) + \
                      ' -input ' + denovoPath
                        #flagfile takes care of inputed chosenPDB, expLL, paramters
                        #-input is helix_denovo.sdef on command line
                        #fibril.pdb, intensity.txt(LLout) and Score (for making chi-sq)+ scoreweights (ignore) outputs specified in flagfile
            subprocess.call(command, shell=True)

        except:  #subprocess.CalledProcessError:  !causes error if added!
            pass


        #LayerLinesToImage
        try:
            #will run from this dir, so local output
            command = './LayerLinesToImage.py' + \
                      ' -e ' + str(Qobject3.EXPupload) + \
                      ' -s ' + intensityPath + \
                      ' -o ' + LLpicPath   #need to modify program or have it dump in local dir and mod path

            subprocess.call(command, shell=True)

        except:  #subprocess.CalledProcessError:    !causes error if added!
            pass


        #Derive Chisq
        #note! if no expLL (just grid.dat) , then score should be empty and no chisq made!!!!!
        Chisq=findChisq(scorePath, Qobject.username)   #parses Score file, which was produced by Rosetta


        #Save Results
        #************
        #load inputs and  results to dbResults
        addResults = dbResults(username=Qobject.username,
                               PDBused=chosenPDB,
                               experimentalData= Qobject3.EXPupload,
                               turns=Qobject4.turns,
                               units=Qobject4.units,
                               rise=Qobject4.rise,
                               rescutL=Qobject4.rescutL,
                               rescutH=Qobject4.rescutH,
                               LorR=Qobject4.LorR,
                               rfactor=Qobject4B.rfactor,
                               bfactor=Qobject4B.bfactor,
                               bfactorSolv=Qobject4B.bfactorSolv,
                               bfactorSolvK=Qobject4B.bfactorSolvK,
                               qfhtK1 = Qobject4B.qfhtK1,
                               qfhtK2 = Qobject4B.qfhtK2,
                               scscaling = Qobject4B.scscaling,
                               gridR = Qobject4B.gridR,
                               gridZ= Qobject4B.gridZ,
                               gridPhi = Qobject4B.gridPhi,
                               FlagFile=Qobject5.FlagFile,
                               denovo = denovoPath,
                               fibrilPDB = fibrilPDBPath,
                               LLoutput=intensityPath,  #derived from Rosetta
                               LLoutputPic=LLpicPath,  #derived from LLoutput processing
                               Score = scorePath,
                               chisq = Chisq)  #derived from score (see chisq function)
        addResults.save()

    #Make Results object for printing to main
    query = 'SELECT * FROM Inputs_dbresults WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    Qobject6 = dbResults.objects.raw(query)[0]


    #Return used parameters to mainpage
    #**********************************
    toreturn= UsedParam(Qobject6)
    return render(request, 'main.html', toreturn)




#Zip and Send, Zip and download and Clear buttons
#************************************************

#Zips and sends to users email
def EmailResults(request):
    if request.method == 'POST':  #when send results button pushed....
        from django.conf import settings
        from django.core.mail.message import EmailMessage
        from django.contrib.auth.models import User
        #get user email from auth_user db
        query = 'SELECT * FROM auth_user WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject8 =User.objects.raw(query)[0] #db called User in Django, auth_user in SQL
        userEmail = str(Qobject8.email)
        #get user run info
        query2 = 'SELECT * FROM Inputs_dbresults WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject6 =dbResults.objects.raw(query2)[0]
        bodytext = 'Here are your requested results for Run Number ' + str(Qobject6.id) + ' carried out on ' + str(Qobject6.timestamp)
        emailResults = EmailMessage(subject='Results of FAT analysis',
                                    body=bodytext,
                                   from_email= settings.EMAIL_HOST_USER,
                                    to=[userEmail]
                                   )

        #make the zipfile
        Path = ZipIt(request, Qobject6)

        #attach results.zip
        emailResults.attach_file(Path)  #attach the zip file
        emailResults.send()            #need to .send()

        #return to mainpage
        return render(request, 'main.html', {})


#Zips and brings up download window
def DownloadResults(request):
    if request.method == 'POST':   #if download is pressed.....
        #zip Jmol, LL, chisq (score.sc) to email and download
        import os, zipfile
        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper

        #get most recent zip of results
        query = 'SELECT * FROM Inputs_dbresults WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject6 =dbResults.objects.raw(query)[0]

        #make the zipfile
        file = ZipIt(request, Qobject6)

        #code for downloading a file
        wrapper = FileWrapper(open(file, 'rb'))  #'rb' is windows fix
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(file)  #loads in chunks: see FileWrapper
        return response


#clear button defaults all inputs
def Clear(request):
    if request.method == 'POST':   #if clear is pressed....
        #default all possible choices, save to appropriate db
        defDown = dbPDBdown(username=request.user.username, PDBdown='none chosen')
        defDown.save()
        defUp = dbPDBup(username=request.user.username, PDBup='none chosen')
        defUp.save()
        defEXP = dbEXPupload(username=request.user.username, EXPupload='none chosen')
        defEXP.save()
        defPara = dbPara(username=request.user.username, turns=5, units=27, rise=2.9, rescutL=0.0833333333, rescutH=0.3333333333, LorR='R')
        defPara.save()
        defPara2 = dbPara2(username=request.user.username, bfactor=20.0, bfactorSolv=400, bfactorSolvK=0.4, gridPhi=128,
                           gridR=256, gridZ=128, qfhtK1=2.0, qfhtK2=2.2, rfactor='False', scscaling=0.92)
        defPara2.save()
        #now run to default everything
        return render(request, 'main.html', {})




#functions
#*******************************************************************************

#Takes username and file, returns a path to user's Storage file (by month)
def PathMaker(name, filename):
    TodaysDate = datetime.date.today()
    Month = str(TodaysDate.month)
    return '/'.join(['C:/Users/Stephen/Dropbox/PycharmProjects/trydjango18/static_in_pro/media_root/Storage', name, Month, filename])

#Remove paths from files for the zipped results
def removePath(path):
    import ntpath
    trimmed = ntpath.basename(path)  #carefule: does not deal with 'file.txt/' syntax
    return trimmed


#Fetch PDB from RBSC
import urllib.request
def fetch_pdb(Qobject):
    url = 'http://www.rcsb.org/pdb/files/%s.pdb' % Qobject.PDBdown
    FH = urllib.request.urlopen(url)
    byteArray = FH.read()   #note: data still a 'bytearray'
    text = byteArray.decode("utf8") #decode or you get b' bla bla bla'
    filename = Qobject.PDBdown + '.pdb'
    Path = PathMaker(Qobject.username, filename)
    Fout = open(Path, 'w')
    Fout.write(text)# string.txt
    FH.close()
    Fout.close()
    return Path


#convert Score file to chi-square value
def findChisq(Path, username):
    FH = open(Path, 'r')
    lineNo=0
    for line in FH:
        if lineNo == 0:
            lineNo= lineNo +1
            line = line.rstrip()
            words = line.split()
            i=0
            for word in words:
                if word == 'fiberdiffraction':
                    index = i
                i=i+1
        else:
            line = line.rstrip()
            words = line.split()
            Chisq = float(words[index])
            return Chisq
    FH.close()

#List of parameters chosen for a given run:
#used for printing on Main.html and made into file for zipping
def UsedParam(Qobject6):
    used = {'PrintRunNum': 'Current run number: ' + str(Qobject6.id),
          'PrintRunDate': 'Run date: ' + str(Qobject6.timestamp),
          'PrintChosen': 'PDB: ' + removePath(str(Qobject6.PDBused)),
          'PrintEXPupload': 'Optional experimental layerlines: ' + removePath(str(Qobject6.experimentalData)),
          'PrintParaT': 'Turns: ' + str(Qobject6.turns),
          'PrintParaU': 'Units: ' + str(Qobject6.units),
          'PrintParaR': 'Rise: ' + str(Qobject6.rise),
          'PrintRescutL': 'Resolution (L): ' + str(Qobject6.rescutL),
          'PrintRescutH': 'Resolution (H): ' + str(Qobject6.rescutH),
          'PrintLorR': 'Handedness: ' + str(Qobject6.LorR)}
    if Qobject6.bfactor != 20.0:
        used['PrintBfactor'] = 'Bfactor: ' + str(Qobject6.bfactor)
    if Qobject6.bfactorSolv != 400:
        used['PrintBfactorSolv'] = 'BfactorSolv: ' + str(Qobject6.bfactorSolv)
    if Qobject6.bfactorSolvK != 0.4:
        used['PrintBfactorSolvK'] = 'BfactorSolvK: ' + str(Qobject6.bfactorSolvK)
    if Qobject6.qfhtK1 != 2.0:
        used['PrintqfhtK1'] = 'qfhtK1: ' + str(Qobject6.qfhtK1)
    if Qobject6.qfhtK2 != 2.2:
        used['PrintqfhtK2'] = 'qfhtK2: ' + str(Qobject6.qfhtK2)
    if Qobject6.scscaling != 0.92:
        used['Printscscaling'] = 'sc_scaling: ' + str(Qobject6.scscaling)
    if Qobject6.gridR != 256:
        used['PrintgridR'] = 'gridR: ' + str(Qobject6.gridR)
    if Qobject6.gridZ != 128:
        used['PrintgridZ'] = 'gridZ: ' + str(Qobject6.gridZ)
    if Qobject6.gridPhi != 128:
        used['PrintgridPhi'] = 'gridPhi: ' + str(Qobject6.gridPhi)
    if Qobject6.experimentalData != 'none chosen':
         used['PrintChi'] = 'Chi-square: ' + str(Qobject6.chisq)

    #Make a .txt file containing all run parameters
    ParamUsedFile(Qobject6, used)   #saves parameters.txt to user's dir
    #supply this dict to fill in Parameters Used located next to Run button
    return used

#Make UsedParameters a .txt file for downloading
def ParamUsedFile(Qobject6, used):
    Path = PathMaker(Qobject6.username, 'parameters.txt')
    FH = open(Path, 'w')
    FH.write('Files and Parameters used for FAT Run Number ' + str(Qobject6.id))
    FH.write("\n")
    FH.write('User: ' + str(Qobject6.username))
    FH.write("\n\n")
    for key in used:
        FH.write(used[key])
        FH.write("\n")
    FH.close()

#zips the three results files: fibril.pdb, LayerLines.jpg and parameters.txt
#places results.zip in user's folder
def ZipIt(request, Qobject6):
    import zipfile
    #remove old
    import os
    try:
        pathtoold = PathMaker(request.user.username, 'results.zip')
        os.remove(pathtoold)
    except OSError:
        pass
    from Inputs.models import dbResults
    #Make Results object
   # query = 'SELECT * FROM Inputs_dbresults WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    #Qobject6 = dbResults.objects.raw(query)[0]

    #select table columns to send
    fibfile = str(Qobject6.fibrilPDB)
    LLout = str(Qobject6.LLoutputPic)
    parampath = PathMaker(request.user.username, 'parameters.txt')

    #give file a name and location in user's dir
    filename = 'results.zip'
    Path = PathMaker(request.user.username, filename)

    #remove paths
    from os.path import basename
    #buffer = StringIO()
    zipped = zipfile.ZipFile(Path, 'w')
    zipped.write(fibfile, basename(fibfile))
    zipped.write(LLout, basename(LLout))
    zipped.write(parampath, basename(parampath))
    zipped.close()

    return Path



