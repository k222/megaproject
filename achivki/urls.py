from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import logout

from achivki.main.views.login import mylogin
from achivki.main.views.profile import profile
from achivki.main.views.feed import feed
from achivki.main.views.registration import register, losepassword
from achivki.main.views.friends import show_friends,search_friends,add_friends,delete_friends

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'achivki.views.home', name='home'),
    # url(r'^achivki/', include('achivki.foo.urls')),

    url(r'^$', 'django.shortcuts.render', {'template_name': 'stub.html'}),
    url(r'^base$', 'django.shortcuts.render', {'template_name': 'generic/site_base.html'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register$', register),
    url(r'^login$',  mylogin),
    url(r'^logout$', logout, {'template_name': 'logout.html'}),
    url(r'^losepassword$', losepassword),
    url(r'^search_friends$', search_friends),
    url(r'^add_friends$', add_friends),
    url(r'^delete_friends$', delete_friends),
    url(r'^(?P<username>.+)/friends$', show_friends),
    url(r'^feed$', feed),
    url(r'^(?P<username>.+)$', profile, name='profile'),
)
