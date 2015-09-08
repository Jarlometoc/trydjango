"""trydjango18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls.static import static  #since STATIC_URL = '/static/'
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'UserAccounts.views.home', name='home'),   #^$ means nothing (home)
    url(r'^contact/$', 'UserAccounts.views.contact', name = 'contact'),
    url(r'^about/$', 'trydjango18.views.about', name = 'about'),
    #url(r'^accounts/', include('registration.backends.default.urls')),    #register
    url(r'^main/', 'trydjango18.views.main', name = 'main'),   #mainpage
    url(r'^accounts/', include('registration.backends.simple.urls')),  #no registration/confirm etc

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   #just for dev
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   #just for dev

