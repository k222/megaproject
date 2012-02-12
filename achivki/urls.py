from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'achivki.views.home', name='home'),
    # url(r'^achivki/', include('achivki.foo.urls')),

    url(r'^$', 'django.contrib.staticfiles.views.serve', {'path': 'stub.html'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) 
