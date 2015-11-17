from django.conf.urls import patterns, url

#links button specific for running rosetta with the function
urlpatterns = patterns('Run.views',
    url(r'^Testing/$', 'Testing', name='urlTesting'),  #link to Testing function to run Rosetta_programs
    #Regex view-url matcher     inputs.views.xxx function   HTTP url name
)
