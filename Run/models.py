from django.db import models

#Flag files table
class dbFlag(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    username = models.CharField(max_length=10)
    FlagFile = models.CharField(max_length=50)   #just a path, not like FileField

    def __str__(self):
        return self.timestamp, self.username, self.FlagFile



