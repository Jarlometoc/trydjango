#main views to load the various pages
from django.shortcuts import render

def home(request):
  return render(request, 'home.html', {}) #context)

def about(request):
    return render(request, 'about.html', {})

def main(request):
    if request.user.is_authenticated():
        return render(request, 'main.html', {})   #mainpage
    else:
        return render(request, 'home.html', {})


#Results view to collect data from various databases, run Rosetta and save results to results DB
#*************************************************************************************************
import datetime
from Inputs.models import dbPDBdown, dbPDBup, dbEXPupload, dbFlag, dbPara, dbResults
import subprocess


#Main function to collect data from DB's, run Rosetta
def Testing(request):
    if request.method == 'POST':   #if run is pressed....

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
        OUT = '-fiber_diffraction:output'

        #make a list of all variables
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
                         OUT]

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


        #Run make_helix_denovo
        #*********************
        #input units/rise/turns/N=40, plus optional files, returns helix_denovo.sdef- symmetry info for Rosetta

        #optional local files to use when needed, placed in /Storage
        import os.path
        #can try import os, os.system('bash script')
        if os.path.isfile('Storage/symmetry_definition_file'):
            symDef = ' -o ' + 'Storage/symmetry_definition_file'
        else:
            symDef = ''
        if os.path.isfile('Storage/virtual_residues_file'):
            virResid = ' -r ' + 'Storage/virtual_residues_file'
        else:
            virResid = ''

        #just for testing on windows
        command = 'python.exe trydjango18\make_helix_denovo.py' #for testing
        subprocess.call(command, shell=True)
        #make a path variable to denovo for dbResults
        denovoPath = str(PathMaker(Qobject.username, 'helix_denovo.sdef'))

        #for Server
        try:
            #make commandline and run  eg, './make_helix_denovo.py -p 2.9 -n 40 -v 5 -u 27 –c L'
            command = 'python3 trydjango18/make_helix_denovo.py' + \
                      ' -p ' + Qobject4.rise + \
                      ' -u ' + Qobject4.units + \
                      ' -n 40' + \
                      ' -v ' + Qobject4.turns + \
                      ' -c ' + Qobject4.LorR + \
                      symDef + virResid  #optional files, if they exist in Storage/
                      #consider adding mv to user's folder as tail string:
                      #first need denovoPath2 = str(PathMaker(Qobject.username, ''))
                      #  + 'mv Storage/helix_denovo.sdef Storage/' + denovoPath2

            subprocess.call(command, shell=True)

            #make a path variable to denovo for dbResults
            denovoPath = str(PathMaker(Qobject.username, 'helix_denovo.sdef'))

        except:  #subprocess.CalledProcessError:    !causes error if added!
            pass



        #run Rosetta
        #***********
        #qQuery dbFlag and make an object containing everything
        query = 'SELECT * FROM Inputs_dbFlag WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject5 = dbPara.objects.raw(query)[0]


        #Determine if Run is with or without experimental LL
        #***************************************************
        if Qobject3.EXPupload == 'none':  #if without:

            #just for testing on windows
            #send flagfile,username, denovoPath to FakeRosetta and get back a fake LLoutput and chisq
            both = (LLoutputPath, fakeChi) = fakeRosetta(Qobject5.FlagFile, Qobject.username)
            #note: returns a tuple: access LLoutputPath, fakeChi from both by LLoutput=both[0], chisq=both[1]

          #for Server
            #'./score.linuxgccrelease @FlagFilePath'
            try:
                command = 'python3 RosettaTest.py ' + str(Qobject5.FlagFile)
                subprocess.call(command, shell=True)

            except:  #subprocess.CalledProcessError:    !causes error if added!
                pass


        #if experimental LL included:
        else:

            #just for testing on windows
            #send flagfile,username, denovoPath to FakeRosetta and get back a fake LLoutput and chisq
            both = (LLoutputPath, fakeChi) = fakeRosetta(Qobject5.FlagFile, Qobject.username)
            #note: returns a tuple: access LLoutputPath, fakeChi from both by LLoutput=both[0], chisq=both[1]


            #for Server
            #'./score.linuxgccrelease @FlagFilePath'
            try:
                command = 'python3 RosettaTest.py ' + str(Qobject5.FlagFile)
                subprocess.call(command, shell=True)

            except:  #subprocess.CalledProcessError:    !causes error if added!
                pass


            #LayerLinesToImage
            #*****************
            #and a pic that actually will come from LLoutput after processing
            LLoutputPicLocation = 'Storage/bunny.jpg'




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
                               LLoutput=both[0],   #LLoutput and chisq has unique format to get first in the tuple outputted by FakeRosetta
                               LLoutputPic=LLoutputPicLocation,  #derived from LLoutput processing
                               chisq=both[1],
                               FlagFile=Qobject5.FlagFile,
                               denovo = denovoPath)
        addResults.save()


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
    Fout.write(text)# string
    FH.close()
    Fout.close()
    return Path


#fake Rosetta until project moved to server
def fakeRosetta(flagfile, username):
    #first open users Flagfile in user's folder
    FHin = open(flagfile, 'r')
    #'FakeLL.txt' outfile to the user's folder
    Path= PathMaker(username, 'FakeLL.txt')
    FHout = open(Path, 'w')
    for line in FHin:
        line = line.rstrip()
        FHout.write(line + '\n')
    FHin.close()
    FHout.close()
    #and a fake Chisq value....
    FakeChisq = '5.5'
    #return both the path to help LLoutput get inputed into dbResults and the ChiSq
    return (Path, FakeChisq)  #note:returns a tuple