from django.conf.urls import patterns, url

#links buttons specific for viewing/processing Results with their respective functions
urlpatterns = patterns('Results.views',
    url(r'^LoadRun/$', 'LoadRun', name='urlLoadRun'),
    url(r'^ReRun/$', 'ReRun', name='urlReRun'),
    url(r'^EmailResults/$', 'EmailResults', name='urlEmailR'),
    url(r'^DownloadResults/$', 'DownloadResults', name='urlDownR'),
    #Regex view-url matcher     inputs.views.xxx function   HTTP url name
)
