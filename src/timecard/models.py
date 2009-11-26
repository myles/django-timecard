import datetime, time

from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.template.defaultfilters import pluralize
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericRelation

class Employee(models.Model):
	employee = models.ForeignKey(User, related_name='timecard_employee',
		unique=True)
	manager = models.ManyToManyField(User, related_name='timecard_managers')
	
	avg_time_in = models.TimeField(_('average time in'))
	avg_time_out = models.TimeField(_('average time out'))
	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	class Meta:
		verbose_name = _('employee')
		verbose_name_plural = _('employees')
		db_table = 'timecard_employees'
	
	@permalink
	def get_absolute_url(self):
		return ('timecard_user', None, {
			'username': self.employee.username,
		})
	
	def __unicode__(self):
		return u"%s %s" % (self.employee.first_name, self.employee.last_name)
	
	def today_timecard(self):
		TODAY = datetime.date.today()
		return Timecard.objects.get(user=self.employee, date=TODAY)

class Timecard(models.Model):
	user = models.ForeignKey(User, related_name='timecards')
	
	date = models.DateField(_('date'))
	time_in = models.TimeField(_('time in'))
	lunch_out = models.TimeField(_('lunch out'), blank=True, null=True)
	lunch_in = models.TimeField(_('lunch in'), blank=True, null=True)
	time_out = models.TimeField(_('time out'), blank=True, null=True)
	
	notes = GenericRelation(Comment, object_id_field='object_pk')
	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	class Meta:
		verbose_name = _('timecard')
		verbose_name_plural = _('timecards')
		db_table = 'timecards'
		ordering = ('-date', 'date_modified')
		unique_together = (('user', 'date'))
	
	def __unicode__(self):
		return u"%s %s - %s" % (self.user.first_name, self.user.last_name, self.date)
	
	@permalink
	def get_absolute_url(self):
		return ('timecard_weekly', None, {
			'username': self.user.username,
			'year': self.date.year,
			'week': self.date.strftime("%W"),
		})
	
	@property
	def lunch(self):
		if self.lunch_in and self.lunch_out:
			lunch = relativedelta(
				datetime.datetime.combine(self.date, self.lunch_in),
				datetime.datetime.combine(self.date, self.lunch_out)
			)
			
			return "%s.%s" % (lunch.hours, ((lunch.minutes * 100) / 60))
		elif self.lunch_out:
			lunch = relativedelta(
				datetime.datetime.now(),
				datetime.datetime.combine(self.date, self.lunch_out)
			)
			
			return "%s.%s" % (lunch.hours, ((lunch.minutes * 100) / 60))
		else:
			return 0
	
	@property
	def full_hours(self):
		if self.time_out:
			full_time = relativedelta(
				datetime.datetime.combine(self.date, self.time_out),
				datetime.datetime.combine(self.date, self.time_in)
			)
		else:
			full_time = relativedelta(
				datetime.datetime.now(),
				datetime.datetime.combine(self.date, self.time_in)
			)
		
		return "%s.%s" % (full_time.hours, ((full_time.minutes * 100) / 60))
	
	@property
	def hours(self):
		try:
			hours = float(self.full_hours) - float(self.lunch)
		except ValueError:
			hours = float(0)
		return hours
	
	@property
	def display_hours(self):
		if not self.hours == 0:
			return u"%s" % (self.hours)
		else:
			return 0
	
	@property
	def breaks(self):
		return Break.objects.filter(timecard=self).aggregate(models.Sum('duration'))['duration__sum']
	
	@property
	def display_breaks(self):
		hours, minutes = divmod(int(self.breaks), 60)
		
		if hours and minutes == 0:
			return u"%s %s%s" % (hours, 'hour', pluralize(hours))
		elif minutes and hours == 0:
			return u"%s %s%s" % (minutes, 'minute', pluralize(minutes))
		else:
			return u"%s %s%s %s %s%s" % (hours, 'hour', pluralize(hours), minutes, 'minute', pluralize(minutes))

class Break(models.Model):
	timecard = models.ForeignKey(Timecard, verbose_name=_('timecard'))
	duration = models.PositiveIntegerField(_('duration'), help_text='In minutes.')
	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	class Meta:
		verbose_name = _('break')
		verbose_name_plural = _('breaks')
		db_table = 'timecard_breaks'
		ordering = ('-date_added',)
	
	def __unicode__(self):
		return u"%s %s" % (self.timecard, self.duration)
	
	@permalink
	def get_absolute_url(self):
		return ('timecard_weekly', None, {
			'username': self.user.username,
			'year': self.date.year,
			'week': self.date.strftime("%W"),
		})
