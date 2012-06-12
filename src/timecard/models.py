import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from timecard.managers import EntryManager

class Entry(models.Model):
	"""A Timecard Entry."""
	
	date = models.DateField()
	
	start_time = models.TimeField()
	end_time = models.TimeField(blank=True, null=True)
	
	user = models.ForeignKey(User)
	
	objects = EntryManager()
	
	class Meta:
		verbose_name = _('entry')
		verbose_name_plural = _('entries')
		db_table = 'timecard_entries'
		get_latest_by = 'date'
		ordering = ('-date', '-start_time')
	
	def __unicode__(self):
		if self.end_time:
			return u"%s: %s-%s" % (self.date.isoformat(), self.start_time.isoformat(), self.end_time.isoformat())
		else:
			return u"%s: %s" % (self.date.isoformat(), self.start_time.isoformat())
	
	@property
	def difference(self):
		if self.end_time:
			diff = datetime.datetime.combine(self.date, self.end_time) - datetime.datetime.combine(self.date, self.start_time)
		else:
			diff = datetime.datetime.now() - datetime.datetime.combine(self.date, self.start_time)
		
		return float(diff.seconds)