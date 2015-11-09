from django.conf.urls import patterns, url

#links buttons specific for importing data with their respective functions
urlpatterns = patterns('Inputs.views',
    url(r'^importPDBdown/$', 'importPDBdown', name='urlPDBdown'),
    url(r'^importPDBup/$', 'importPDBup', name='urlPDBup'),
    url(r'^importEXP/$', 'importEXP', name='urlEXP'),
    url(r'^importParameters/$', 'importParameters', name='urlParameters'),
    url(r'^importPara2/$', 'importPara2', name='urlPara2'),   #extra parameters
    url(r'^Clear/$', 'Clear', name='urlClear'),
    #Regex view-url matcher     inputs.views.xxx function   HTTP url name
)

