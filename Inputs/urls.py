from django.conf.urls import patterns, url

#Allows functions to be accessed from main.html via the primary urls.py
urlpatterns = patterns('Inputs.views',
    url(r'^importPDBdown/$', 'importPDBdown', name='urlPDBdown'),
    url(r'^importPDBup/$', 'importPDBup', name='urlPDBup'),
    url(r'^importEXP/$', 'importEXP', name='urlEXP'),
    url(r'^importParameters/$', 'importParameters', name='urlParameters'),
    #Regex view-url matcher     inputs.views.xxx function   HTTP url name
)

