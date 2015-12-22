from django.db import models

#Model for results
#note this model is used by Results.admin.py to display the Results table

#Results files table (from Rosetta_programs)
class dbResults(models.Model):
    mostRes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    PDBused = models.CharField(max_length=100)
    experimentalData = models.CharField(max_length=100)
    jobname = models.CharField(max_length=50)
    turns = models.FloatField(default=5)
    units = models.FloatField(default=27)
    rise = models.FloatField(default=2.9)
    rescutL=models.FloatField(default=0.0833333333)
    rescutH=models.FloatField(default=0.3333333333)
    LorR = models.CharField(max_length=1, default='R')
    rfactor=models.CharField(max_length=5, default='False')
    bfactor=models.FloatField(default=20.0)
    bfactorSolv=models.FloatField(default=400)
    bfactorSolvK=models.FloatField(default=0.4)
    qfhtK1 = models.FloatField(default=2.0)
    qfhtK2 = models.FloatField(default=2.2)
    scscaling = models.FloatField(default=0.92)
    gridR = models.IntegerField(default=256)
    gridZ= models.IntegerField(default=128)
    gridPhi = models.IntegerField(default=128)
    R_step = models.FloatField(default=0.001)
    layer_lines = models.IntegerField(default=20)
    intensity = models.CharField(max_length=100, default='empty')
    fibrilPDB = models.CharField(max_length=100, default='empty')
    LLoutputPic = models.CharField(max_length=100, default='Storage/bunny.jpg')
    chisq = models.FloatField(default=0)

    #for class instances of the model
    def __str__(self):
        return self.mostRes, \
               self.timestamp, \
               self.username, \
               self.jobname, \
               self.PDBused, \
               self.experimentalData, \
               self.turns, \
               self.units, \
               self.rise, \
               self.rescutL, \
               self.rescutH, \
               self.LorR, \
               self.rfactor, \
               self.bfactor, \
               self.bfactorSolv, \
               self.bfactorSolvK, \
               self.qfhtK1, \
               self.qfhtK2,\
               self.scscaling, \
               self.gridR, \
               self.gridZ, \
               self.gridPhi, \
               self.R_step, \
               self.layer_lines, \
               self.intensity, \
               self.fibrilPDB, \
               self.LLoutputPic,\
               self.chisq

               
#DB for loading older results
class dbrerun(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    runNum = models.IntegerField(default=1)
    
    def __str__(self):
        return self.timestamp, self.username, self.runNum