#URLS for pages

from django.conf.urls.static import static  #since STATIC_URL = '/static/'
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url


urlpatterns = [
    #Regex view-url matcher     inputs.views.xxx function   HTTP url name
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'trydjango18.views.home', name='home'),   #^$ means nothing (home)
    url(r'^contact/$', 'UserAccounts.views.contact', name = 'contact'),
    url(r'^about/$', 'trydjango18.views.about', name = 'about'),
    url(r'^main/', 'trydjango18.views.main', name = 'main'),   #mainpage
    url(r'^accounts/', include('registration.backends.simple.urls')),  #no registration/confirm etc
    url(r'^Inputs', include('Inputs.urls')),  #link to the Inputs urls
    url(r'^Testing/$', 'trydjango18.views.Testing', name='urlTesting'),  #link to Testing function to run Rosetta
    url(r'^Clear/$', 'trydjango18.views.Clear', name='urlClear'),
    url(r'^ReRun/$', 'trydjango18.views.ReRun', name='urlReRun'),
    url(r'^EmailResults/$', 'trydjango18.views.EmailResults', name='urlEmailR'),
    url(r'^DownloadResults/$', 'trydjango18.views.DownloadResults', name='urlDownR'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   #just for dev
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   #just for dev

