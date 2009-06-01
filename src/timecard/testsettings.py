DEBUG = True
DEBUG_TEMPLATE = True
SITE_ID = 1
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/django-timecard-devel.db'
INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.comments',
	'django.contrib.contenttypes',
	'timecard',
]
ROOT_URLCONF = 'timecard.testurls'
TIME_ZONE = 'Canada/Eastern'