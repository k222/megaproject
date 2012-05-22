from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import logout

from achivki.main.views.login import mylogin
from achivki.main.views.profile import profile
from achivki.main.views.feed import feed
from achivki.main.views.registration import register, lost_password
from achivki.main.views.friends import show_friends,search_friends,add_friends,delete_friends
from achivki.main.views.settings import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin interface
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # title page
    url(r'^$', 'django.shortcuts.render', {'template_name': 'title.html'}),

    # registration
    url(r'^register$', register),
    url(r'^login$',  mylogin),
    url(r'^logout$', logout, {'template_name': 'logout.html'}),
    url(r'^lost_password$', lost_password),

    # pony countdown
    url(r'^pony_countdown$', 'django.shortcuts.render', {'template_name': 'pony_countdown.html'}),

    # debug hook for rendering any template
    url(r'^template/(?P<template_name>.+)$', 'django.shortcuts.render'),

    # friends
    url(r'^search_friends$', search_friends),
    url(r'^add_friends$', add_friends),
    url(r'^delete_friends$', delete_friends),
    url(r'^settings$', settings),
    url(r'^feed$', feed),
    url(r'^(?P<username>.+)/friends$', show_friends),
    url(r'^(?P<username>.+)$', profile, name='profile'),
)
