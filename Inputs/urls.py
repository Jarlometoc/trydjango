from django.conf.urls import patterns, url

#Allows functions to be accessed from main.html via the primary urls.py
urlpatterns = patterns('Inputs.views',
    url(r'^importPDBdown/$', 'importPDBdown', name='importPDBdown'),
    url(r'^importPDBup/$', 'importPDBup', name='importPDBup'),
    url(r'^importEXP/$', 'importEXP', name='importEXP'),
    url(r'^importParameters/$', 'importParameters', name='importParameters'),
)

