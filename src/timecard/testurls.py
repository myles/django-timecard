from django.contrib import admin
from django.conf.urls.defaults import patterns, url, include

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	
	url(r'^timecard/', include('timecard.urls')),
)