from django.contrib import admin
from Results.models import dbResults

#without this, the data is in one big clump in admin
class ResultsAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'timestamp',
                    'username',
                    'jobname',
                    'PDBused',
                    'experimentalData',
                    'turns',
                    'units',
                    'rise',
                    'rescutL',
                    'rescutH',
                    'LorR',
                    'rfactor',
                    'bfactor',
                    'bfactorSolv',
                    'bfactorSolvK',
                    'qfhtK1',
                    'qfhtK2',
                    'scscaling',
                    'gridR',
                    'gridZ',
                    'gridPhi',
                    'fibrilPDB',
                    'LLoutputPic',
                    'chisq']
    class Meta:
        model = dbResults

admin.site.register(dbResults, ResultsAdmin)  #add new admin.site.register lines for each db to view