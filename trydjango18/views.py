#main views to load the various pages
from django.shortcuts import render
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
from Inputs.models import dbPDBdown, dbPDBup, dbEXPupload, dbFlag, dbPara, dbResults
import subprocess


#Main function
#*************
def Testing(request):
    if request.method == 'POST':   #if Run is pressed....

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
       #These are currently default
        Rfac = '-fiber_diffraction:rfactor_refinement '+ str(Qobject4.rfactor)    #If set R factor instead of chi2 is used in scoring and derivatives calculations
        AtomicBF = '-fiber_diffraction::b_factor '+ str(Qobject4.bfactor)    #Atomic B-factor
        Solv = '-fiber_diffraction::b_factor_solv '+ str(Qobject4.bfactorSolv)   #temperature factor that accounts for the disordered solvent
        SolvK = '-fiber_diffraction::b_factor_solv_K '+ str(Qobject4.bfactorSolvK)   #scale factor that adjust average solvent scattering intensity
        K1 = '-fiber_diffraction:qfht_K1 '+ str(Qobject4.qfhtK1)    #Hankel transform K1 parameter
        K2 = '-fiber_diffraction:qfht_K2 '+ str(Qobject4.qfhtK2)      #Hankel transform K1 parameter
        SC = '-edensity:sc_scaling '+ str(Qobject4.scscaling)    #Hankel transform K1 parameter
        GridR = '-fiber_diffraction:grid_r '+ str(Qobject4.gridR)     #Grid size r, should be bigger than radius of molecule
        GridZ = '-fiber_diffraction:grid_z '+ str(Qobject4.gridZ)     #Grid size z, should be bigger than molecule span in z direction
        GridPhi = '-fiber_diffraction:grid_phi '+ str(Qobject4.gridPhi)    #Grid size phi, change if higher accuracy is needed
        #output for Rosetta
        fibPDBout = '-out:file ' + PathMaker(Qobject.username, 'fibPDB')
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
        fibrilPDBPath = str(PathMaker(Qobject.username, 'fibPDB'))
        scorePath = str(PathMaker(Qobject.username, 'score.sc'))
        intensityPath = str(PathMaker(Qobject.username, 'intensity.txt'))
        LLpicPath = str(PathMaker(Qobject.username, 'LLoutputPic'))


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
                        #fibPDB, intensity.txt(LLout) and Score (for making chi-sq)+ scoreweights (ignore) outputs specified in flagfile
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
                               rfactor=Qobject4.rfactor,
                               bfactor=Qobject4.bfactor,
                               bfactorSolv=Qobject4.bfactorSolv,
                               bfactorSolvK=Qobject4.bfactorSolvK,
                               qfhtK1 = Qobject4.qfhtK1,
                               qfhtK2 = Qobject4.qfhtK2,
                               scscaling = Qobject4.scscaling,
                               gridR = Qobject4.gridR,
                               gridZ= Qobject4.gridZ,
                               gridPhi = Qobject4.gridPhi,
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


    #Return to mainpage
    #Display next to RUN button
    #**************************
    return render(request, 'main.html',
         {'PrintEXPupload': Qobject3.EXPupload,
         'PrintParaT': Qobject4.turns,
         'PrintParaU': Qobject4.units,
         'PrintParaR': Qobject4.rise,
         'PrintChosen': chosenPDB,
         'PrintChi': Qobject6.chisq
         })


def Clear(request):
    if request.method == 'POST':   #if clear is pressed....
        #Add to tables so default values are most recent entry
        #'run' empty so nothing in Jmol, LL or chisq
        return render(request, 'main.html', {})

def EmailResults(request):
    if request.method == 'POST':
        #run ZipIt to open dbResults, pull out fibPDB, LLPic and chisq, zip it, store in user's dir
        Path = ZipIt(request)
        #Email zipped file to user
        from django.conf import settings
        from django.core.mail.message import EmailMessage
        emailResults = EmailMessage(subject='Results of FAT analysis',
                                    body='Here are your requested results',
                                   from_email= settings.EMAIL_HOST_USER,
                                    to=['shburleigh@gmail.com'],
                                   )
        emailResults.attach_file(Path)  #attach the zip file
        emailResults.send()            #need to .send()

        #return to mainpage
        return render(request, 'main.html', {})


def DownloadResults(request):
    if request.method == 'POST':
        #zip Jmol, LL, chisq (score.sc) to email and download
        return render(request, 'main.html', {})



#functions
#*******************************************************************************

#Takes username and file, returns a path to user's Storage file (by month)
def PathMaker(name, filename):
    TodaysDate = datetime.date.today()
    Month = str(TodaysDate.month)
    return '/'.join(['C:/Users/Stephen/Dropbox/PycharmProjects/trydjango18/static_in_pro/media_root/Storage', name, Month, filename])


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



def ZipIt(request):
    import zipfile
    from Inputs.models import dbResults
    #Make Results object
    query = 'SELECT * FROM Inputs_dbresults WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    Qobject6 = dbResults.objects.raw(query)[0]
    #select table columns you want to send
    fibfile = str(Qobject6.fibrilPDB)
    LLout = str(Qobject6.LLoutputPic)
    score= str(Qobject6.Score)
    #give file a name and location in user's dir
    Path = PathMaker(request.user.username, 'results.zip')
    #make zipcontainer and fill with zipped files
    zipped = zipfile.ZipFile(Path, 'w')
    zipped.write('C:/Users/Stephen/Dropbox/PycharmProjects/trydjango18/static_in_pro/media_root/Storage/bunny.jpg')
    #zipped.write(fibfile)  #fibrilPDB
    #zipped.write(LLout)  #LLPic
    #zipped.write(score) #chi-sq
    zipped.close()
    return Path

