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


#**************************************************'

#set storage path for files to include username and month number
import datetime
def PathMaker(name, filename):
    TodaysDate = datetime.date.today()
    Month = str(TodaysDate.month)
    return '/'.join(['C:/Users/Stephen/Dropbox/PycharmProjects/trydjango18/static_in_pro/media_root/Storage', name, Month, filename])


#just for testing
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from Inputs.models import dbPDBdown, dbPDBup, dbEXPupload, dbFlag, dbPara, dbResults
import subprocess

def Testing(request):
    #use sql to search DB: consider SQL injection attacks here

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


    #Identify the most current upload or download by timestamp
    if Qobject.timestamp > Qobject2.timestamp:
        chosenPDB = fetch_pdb(Qobject)

    else:
        chosenPDB = Qobject2.PDBup


    #gather data and submit to Rosetta

    #parameters
    PDB = '-in:file:s '+ str(chosenPDB)   #the chosen PDB, based on most recent timestamp
    EXP =  '-fiber_diffraction:layer_lines '+ str(Qobject3.EXPupload)     #File containing fiber diffraction layer lines
    Units = '-fiber_diffraction:a '+ str(Qobject4.units)     #number of units
    Turns = '-fiber_diffraction:b '+ str(Qobject4.turns)    #number of turns
    Rise = '-fiber_diffraction:p '+ str(Qobject4.rise)     #If specified, subunit rise is taken from input, otherwise is calculated by the program

    #These are currently default
    Lcutoff = '-fiber_diffraction:resolution_cutoff_low 0.0833333333' #Resolution cutoff 12Å
    Hcutoff = '-fiber_diffraction:resolution_cutoff_high 0.3333333333' #Resolution cutoff 3Å
    Rfac = '-fiber_diffraction:rfactor_refinement'    #If set R factor instead of chi2 is used in scoring and derivatives calculations
    AtomicBF = '-fiber_diffraction::b_factor 20.0'    #Atomic B-factor
    Solv = '-fiber_diffraction::b_factor_solv 400'   #temperature factor that accounts for the disordered solvent
    SolvK = '-fiber_diffraction::b_factor_solv_K 0.4'   #scale factor that adjust average solvent scattering intensity
    K1 = '-fiber_diffraction:qfht_K1 2.0'    #Hankel transform K1 parameter
    K2 = '-fiber_diffraction:qfht_K2 2.2'    #Hankel transform K1 parameter
    SC = '-edensity:sc_scaling 0.92'    #Hankel transform K1 parameter
    GridR = '-fiber_diffraction:grid_r 256'     #Grid size r, should be bigger than radius of molecule
    GridZ = '-fiber_diffraction:grid_z 128'     #Grid size z, should be bigger than molecule span in z direction
    GridPhi = '-fiber_diffraction:grid_phi 128'    #Grid size phi, change if higher accuracy is needed
    OUT = '-fiber_diffraction:output'    #Saves simulated intensities to a file

    ParameterList = [PDB,
                     EXP,
                     Units,
                     Turns,
                     Rise,
                     Lcutoff,
                     Hcutoff,
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

    #make the Flags file
    filename = Qobject.username + '_Flags'
    Path = PathMaker(Qobject.username, filename)
    FHout = open(Path, 'w')
    for item in ParameterList:
        FHout.write("%s\n" % item)
    FHout.close()

    #now save path to dbFlags
    addFlag = dbFlag(username=Qobject.username, FlagFile=Path)
    addFlag.save()

    #send to Rosetta
    query = 'SELECT * FROM Inputs_dbFlag WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
    Qobject5 = dbPara.objects.raw(query)[0]
    FlagFilePath = Qobject5.FlagFile
    #quick function to make a fake LLoutput and chisq for testing
    both = (LLoutputPath, fakeChi) = fakeRosetta(FlagFilePath, Qobject.username)  #note:returns a tuple


    #load the results database  PDBused= chosenPDB
    addResults = dbResults(username=Qobject.username, PDBused=chosenPDB, experimentalData= Qobject3.EXPupload, \
                           turns=Qobject4.turns, units=Qobject4.units, rise=Qobject4.rise, LLoutput=both[0], \
                           chisq=both[1], FlagFile=Qobject5.FlagFile)
    addResults.save()


    #likely final code:
    #'./score.linuxgccrelease @FlagFilePath'
    #try:
        #command = 'python3 RosettaTest.py ' + str(FlagFilePath)
        #subprocess.call(command, shell=True)
        #pass
  # except subprocess.CalledProcessError:
       # pass # handle errors in the called executable



    #Display Results on Testing.HTML
    templateObject = get_template('testing.html')
    html = templateObject.render(Context( {'PrintPDBdown': Qobject.PDBdown, #Qobject contains id,PDBdown,timestamp
                                           'PrintPDBup': Qobject2.PDBup,
                                           'PrintEXPupload': Qobject3.EXPupload,
                                           'PrintParaT': Qobject4.turns,
                                           'PrintParaU': Qobject4.units,
                                           'PrintParaR': Qobject4.rise,
                                           'PrintChosen': chosenPDB        #this is the PDB sent to Rosetta
                                           } ))
    return HttpResponse(html)


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