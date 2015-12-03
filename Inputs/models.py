#Models for Inputs
#*****************

#imports
from django.db import models
from django.core.validators import RegexValidator  #for regex to make PDBdown exactly 4 length
from trydjango18.views import PathMaker2  #gives path to up- and downloads (user,month)


#Models:
#*******
#each button for the inports on the mainpage is a seperate table

#download from RCSB
class dbPDBdown(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    PDBdown = models.CharField(validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='nomatch')], max_length=4)

    def __str__(self):
        return self.timestamp, self.username, self.PDBdown

#upload local file
class dbPDBup(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    PDBup = models.FileField(upload_to=PathMaker2)

    def __str__(self):
        return self.timestamp, self.username, self.PDBup

#upload experimental LL data
class dbEXPupload(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    EXPupload = models.FileField(upload_to=PathMaker2)

    def __str__(self):
        return self.timestamp, self.username, self.EXPupload

#parameters
class dbPara(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    jobname = models.CharField(max_length=50, default= ' ')
    turns = models.FloatField(default=27)
    units = models.FloatField(default=5)
    rise = models.FloatField(default=2.9)
    rescutL = models.FloatField(default=0.0833333333)
    rescutH = models.FloatField(default=0.333333333)
    LorR = models.CharField(max_length=1, default='R')


    def __str__(self):
        return self.timestamp, self.username, self.jobname, self.turns, self.units, self.rise, self.rescutL, self.rescutH, self.LorR

#additional parameters
class dbPara2(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    rfactor = models.CharField(max_length=5, default='False')
    bfactor = models.FloatField(default=20)
    bfactorSolv = models.FloatField(default=400)
    bfactorSolvK = models.FloatField(default=0.4)
    qfhtK1 = models.FloatField(default=2.0)
    qfhtK2 = models.FloatField(default=2.2)
    scscaling = models.FloatField(default=0.92)
    gridR = models.IntegerField(default=256)
    gridZ= models.IntegerField(default=128)
    gridPhi = models.IntegerField(default=128)
    R_step = models.FloatField(default=0.001)
    layer_lines = models.IntegerField(default=20)



    def __str__(self):
        return self.timestamp, self.username,  \
     self.rfactor, self.bfactor, self.bfactorSolv, self.bfactorSolvK, self.qfhtK1, \
     self.qfhtK2, self.scscaling, self.gridR, self.gridZ, self.gridPhi, self.R_step, self.layer_lines


