from datetime import datetime   #need to add for datetime default
from django.db import models
class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length = 120, blank = False, null= True)  #blank=False means its req
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    #..add means save this timestamp when created, auto_now is just whenever after initial db creation
    updated = models.DateTimeField(default=datetime.now, blank=True)  #this needs a default

    def __str__(self): #__unicode__ for lower versions
        return self.email
