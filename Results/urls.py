from django.conf.urls import patterns, url

#links buttons specific for viewing/processing Results with their respective functions
urlpatterns = patterns('Results.views',
    url(r'^LoadRun/$', 'LoadRun', name='urlLoadRun'),
    url(r'^ReRun/$', 'ReRun', name='urlReRun'),
    url(r'^EmailResults/$', 'EmailResults', name='urlEmailR'),
    url(r'^DownloadResults/$', 'DownloadResults', name='urlDownR'),
     #Regex view-url matcher     inputs.views.xxx function   HTTP url name
    
    # original: (r'^jmol/(?P<path>.*)$', 'django.views.static.serve', {'document_root': BASE_PATH + 'site_media/jmol/', 'show_indexes': True}),
    #(r'^jsmol/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static_in_pro/jsmol/'}),
   
)
