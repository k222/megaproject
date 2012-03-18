from django.conf.urls.defaults import patterns, include, url

from achivki.main.views.registration import register,losepassword
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'achivki.views.home', name='home'),
    # url(r'^achivki/', include('achivki.foo.urls')),

    url(r'^$', 'django.shortcuts.render', {'template_name': 'stub.html'}),
    url(r'^base$', 'django.shortcuts.render', {'template_name': 'base.html'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register$', register),
    url(r'^login$',  login, {'template_name': 'login.html'}),
    url(r'^logout$', logout, {'template_name': 'logout.html'}),
    url(r'^losepassword$', losepassword),
) 
