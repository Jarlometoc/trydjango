#Run denovo, Rosetta and LayerLinesToImage.  Save results to results table
#*************************************************************************

#imports
#*******
from django.shortcuts import render
from Inputs.models import dbPDBdown, dbPDBup, dbEXPupload, dbPara, dbPara2
from Results.models import dbResults
from .models import dbFlag
import os
from trydjango18.views import PathMaker, removePath
from Results.views import getRunDict, getLoadDict
from static_in_pro.media_root.Rosetta_programs.make_helix_denovo import Helixer
from static_in_pro.media_root.Rosetta_programs.syn_grid import makeDefExp
from static_in_pro.media_root.Rosetta_programs.layerLinesToImage import LLTI
import datetime

#Main function
#*************
def Testing(request):

    #get loaded Results data, if any, for the Testing Refresh, otherwise it will blank
    #should be blank prior to first load request
    rerun = getLoadDict(request.user.username)

    #include ToBeRun dictionary from inputs
    ToBeRunDict = getRunDict(request.user.username)

    #if Run is pressed....
    if request.method == 'POST':   

        #check here if no PDB
        #if ...

        #SQL to make query objects for each table
        #****************************************
        #download
        query = 'SELECT * FROM Inputs_dbpdbdown WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject = dbResults.objects.raw(query)[0]

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
            chosenPDB = 'static_in_pro/media_root/' + str(Qobject2.PDBup)

        #make grid.dat
        #*************
        #default expLL: Need Hcutoff and Lcutoff (as floating numbers)
        #output is grid.dat, which is used to for making EXP in flag file
        makeDefExp(Qobject.username, float(Qobject4.rescutH), float(Qobject4.rescutL))

        #Make FlagsFile using the query objects
        #**************************************
        #overwrite for reruns
        overwrite = '-out:overwrite'
        #db path for rosetta, otherwise its default, somewhere on server
        db = '-database /home/stephen/Project/trydjango/static_in_pro/media_root/Storage/database'
        #add sdef from helix_denovo output
        sdef = '-symmetry:symmetry_definition ' + '/home/stephen/Project/trydjango/' + PathMaker(Qobject.username, 'helix_denovo.sdef')
        #needed for some reason
        extra = '-symmetry:initialize_rigid_body_dofs'      
        #the chosen PDB, based on most recent timestamp
        PDB = '-in:file:s '+ '/home/stephen/Project/trydjango/' + str(chosenPDB)   
        #if experimental is 'none chosen', grid.dat needs to be used in its place
        if 'none chosen' in str(Qobject3.EXPupload):
            EXP = '-fiber_diffraction:layer_lines ' + '/home/stephen/Project/trydjango/' + PathMaker(Qobject.username, 'grid.dat')
        else:
            EXP = '-fiber_diffraction:layer_lines ' + 'static_in_pro/media_root/' + str(Qobject3.EXPupload)
        #generic inputs
        Units = '-fiber_diffraction:a '+ str(Qobject4.units)     #number of units
        Turns = '-fiber_diffraction:b '+ str(Qobject4.turns)    #number of turns
        Rise = '-fiber_diffraction:p '+ str(Qobject4.rise)     #If specified, subunit rise is taken from input, otherwise is calculated by the program
        Lcutoff = '-fiber_diffraction:resolution_cutoff_low '+ str(Qobject4.rescutL)  #Resolution cutoff 12�
        Hcutoff = '-fiber_diffraction:resolution_cutoff_high '+ str(Qobject4.rescutH)  #Resolution cutoff 3�
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
        #output for Rosetta_programs
        fibPDBout = '-out:output ' 
        outputpath = '-out:path:pdb ' + PathMaker(Qobject.username, '')  #Rosetta decides name of fibrilPDB, we can only prefix it
        prefix = '-out:prefix ' + 'RUN' + str(tagOutput(request)) + '_'
        suffix = '-out:suffix '
        LLout = '-fiber_diffraction:output_fiber_spectra' #+ PathMaker(Qobject.username, 'Intensity.txt')   #to make LLpic, stored in user's folder'
        Score = '-out:file:scorefile ' + '/home/stephen/Project/trydjango/' + PathMaker(Qobject.username, 'score.sc')
        scoreWeights = '-score:weights /home/stephen/Project/trydjango/static_in_pro/media_root/Rosetta_files/fiberdiffraction.txt'  #text file is only “fiberdiffraction 1”
               
        #make a list of the above variables
        ParameterList = [
                         overwrite,
                         db,
                         sdef,
                         extra,
                         PDB,
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
                         fibPDBout,
                         LLout,
                         Score,
                         prefix,
                         suffix,
                         outputpath,
                         scoreWeights]

        #make the Flags file, tagged with username, placed in user's folder
        filename = str(Qobject.username) + '_Flags'
        Path = PathMaker(Qobject.username, filename)
        FHout = open(Path, 'w')
        for item in ParameterList:
            FHout.write("%s\n" % item)
        FHout.close()
        #now save path to dbFlags
        addFlag = dbFlag(username=Qobject.username, FlagFile=Path)
        addFlag.save()

        #Path variables for dbResults  **make sure their -creation- also points to same user dir
        #Paths needed for make_helix_denovo
        denovoPath = str(PathMaker(Qobject.username, 'helix_denovo.sdef'))
        virtualsPath = str(PathMaker(Qobject.username, 'virtuals.pdb'))
        #for Rosetta     
        fibrilPDBPath = str(PathMaker(Qobject.username, fibRename(request, chosenPDB))) #Rosetta outputs odd name, so need function to match it for db
        intensityPath = str(PathMaker3(Qobject.username, 'Intensity.txt')) #need special path correction; see PathMaker3
        scorePath = str(PathMaker(Qobject.username, 'score.sc'))
        #for layerlinestoimage
        LLpicPath = str(PathMaker(Qobject.username, 'layerlines_run' + str(tagOutput(request)) + '.png')) #note: need to save this file for future load requests

        #Run make_helix_denovo:
        #*********************
        #input: units/rise/turns/N=40, plus path to .sdef output, path to virtualPDB
        helixer = Helixer(float(Qobject4.rise), int(40), int(Qobject4.turns), int(Qobject4.units), denovoPath, virtualsPath)
        #Executing pipeline
        helixer.execute()
        helixer.write()
        helixer.writePDBlines()
        #output of helix_denovo.sdef 'symmetry definition file'
        #output of virtuals.pdb: virtual_residues_file also made each run: for diagnostics

        #run Rosetta
        #***********
        #query dbFlag and make an object containing everything
        query = 'SELECT * FROM Run_dbflag WHERE username = "'+request.user.username+'" ORDER BY id DESC LIMIT 1'
        Qobject5 = dbFlag.objects.raw(query)[0]

        #inputs: see Flagfile
        program = '/home/stephen/Project/trydjango/static_in_pro/media_root/Rosetta_programs/score.static.linuxgccrelease'
        addflag = '@' + '/home/stephen/Project/trydjango/' + str(Qobject5.FlagFile) #need to add prefix path, since not django       
        together = program + ' ' + addflag
        Path2 = PathMaker(Qobject.username, 'cmd')
        FHout2 = open(Path2, 'w')
        FHout2.write("%s\n" % together)
        FHout2.close()
        os.system('chmod 775 ' + Path2)
        os.system(Path2)
        #outputs: fibril.pdb, intensity.txt(LLout), score.sc (for making chi-sq)+ scoreweights (ignore)
       
        #move intensity.txt from Project/tryjango to user dir
        moveInten(request)
       
        #Run LayerLinesToImage
        #*********************
        #output: layerlines.png stored in LLpic attribute
        output = PathMaker(Qobject.username, 'layerlines_run' + str(tagOutput(request)) + '.png')
        experimental = str(Qobject3.EXPupload)
        layerlines = LLTI(intensityPath, experimental, output)
        layerlines.convert_to_image()

        #Derive Chisq
        #************
        #note! if no expLL (just grid.dat) , then score should be empty and no chisq made!!!!!
        Chisq=findChisq(scorePath, Qobject.username)   #parses Score file, which was produced by Rosetta_programs

        #Save Results
        #************
        #load inputs and  results to dbResults
        addResults = dbResults(username=Qobject.username,
                               PDBused=chosenPDB,
                               experimentalData= Qobject3.EXPupload,
                               jobname=Qobject4.jobname,
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
                               fibrilPDB = fibrilPDBPath,
                               LLoutputPic=LLpicPath,  #derived from LLtoImage
                               chisq = Chisq)  #derived from Score (see chisq function)
        addResults.save()

    #RENDER
    #toreturn= UsedParam(Qobject6)      #note! UsedParam also includes newrundict.txt results for 'to be run' files/para
    return render(request, 'main.html', {'ToBeRunHTML' : ToBeRunDict, 'resultsHTML': rerun})


#Run-related functions
#*********************

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
                if word == 'fiberdiffraction': #chi-sq should be just below this string
                    index = i
                i=i+1
        else:
            line = line.rstrip()
            words = line.split()
            Chisq = float(words[index])
            return Chisq
    FH.close()

    
#tag output files of Rosetta and LLtoImage; this function makes the approp run number
def tagOutput(request):
    try:
        query = 'SELECT * FROM Results_dbresults WHERE username = "' + request.user.username + '" ORDER BY id DESC LIMIT 1'
        Qobject6 = dbResults.objects.raw(query)[0]
        run = str(int(Qobject6.id)+1) #run id will be one more than last run id
    except:
        run = '1'  #if first run
    return run

#Temp fix for Intensity.txt landing in Project/trydjango/
def moveInten(request):
    try:
        templocale = '/home/stephen/Project/trydjango/Intensity.txt'
        genericpath = '/home/stephen/Project/trydjango/'
        userdir = PathMaker(request.user.username, '')
        fullpath = 'mv ' + templocale + ' ' + genericpath + userdir
        os.system(fullpath)
    except:
        pass

#need to mod intensity.txt paths- got double 'static_in_pro/media_root' with PathMaker
def PathMaker3(name, filename):
    TodaysDate = datetime.date.today()
    Month = str(TodaysDate.month)
    return '/'.join(['Storage', name, Month, filename])  #remove 'static_in_pro/media_root'   


#rename fibrillarPDB output to what Rosetta outputs
def fibRename(request, chosenPDB):
    #get run number
    runnum=tagOutput(request)
    #get chosenPDB name
    name = removePath(chosenPDB)
    name = name[:-4]
    #add Rosettas silly suffix
    suffix = '_0001.pdb'
    PathtofibrilPDB = 'RUN' + runnum + '_' + name + suffix
    return PathtofibrilPDB
    
    
    

    