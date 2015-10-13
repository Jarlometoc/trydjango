from django.conf.urls import patterns, url

#Allows functions (to gather form data) to be accessed from main.html
#Note: this group of urls connects to the primary urls.py via 'url(r'^Inputs', include('Inputs.urls'))'
urlpatterns = patterns('Inputs.views',
    url(r'^importPDBdown/$', 'importPDBdown', name='urlPDBdown'),
    url(r'^importPDBup/$', 'importPDBup', name='urlPDBup'),
    url(r'^importEXP/$', 'importEXP', name='urlEXP'),
    url(r'^importParameters/$', 'importParameters', name='urlParameters'),
    #Regex view-url matcher     inputs.views.xxx function   HTTP url name
)

