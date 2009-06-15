from django.conf.urls.defaults import *

urlpatterns = patterns('timecard.views',
	url(r'^$',
		view = 'index',
		name = 'timecard_homepage',
	),
)