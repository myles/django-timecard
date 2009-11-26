import datetime

from dateutil import parser

from django import forms
from django.forms.widgets import Input

class TimeWidget(Input):
	format = '%I:%M %p' # '12:20 PM'
	
	def __init__(self, attrs=None, format=None):
		self.attrs = {'class': 'vTimeField', 'size': '8', 'autocomplete': 'off'}
		super(TimeWidget, self).__init__(self.attrs)
		if format:
			self.format = format
	
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		
		if hasattr(value, 'strftime'):
			value = value.strftime(self.format)
		
		return super(TimeWidget, self).render(name, value, attrs)

class FuzzyTimeField(forms.Field):
	widget = TimeWidget
	
	def clean(self, value):
		super(FuzzyTimeField, self).clean(value)
		if value in (None, ''):
			return None
		
		if isinstance(value, datetime.time):
			return value
		else:
			try:
				return parser.parse(value).time()
			except ValueError, e:
				raise ValidationError(u'Enter a valid date and time')

class TimecardForm(forms.Form):
	date = forms.DateField(label=u'Date', widget=forms.HiddenInput)
	time_in = FuzzyTimeField(label=u'Time in', required=True)
	lunch_out = FuzzyTimeField(label=u'Lunch out', required=False)
	lunch_in = FuzzyTimeField(label=u'Lunch in', required=False)
	time_out = FuzzyTimeField(label=u'Time out', required=False)
	
	fm_name = forms.CharField(widget=forms.HiddenInput, initial=u'TimecardForm')

BREAK_DURATION_CHOICES = (
	(5, '5 min'),
	(10, '10 min'),
	(15, '15 min'),
	(20, '20 min'),
	(30, '30 min'),
	(40, '40 min'),
	(50, '50 min'),
	(60, '1 hour'),
)

class BreakForm(forms.Form):
	duration = forms.ChoiceField(label=u'Duration', choices=BREAK_DURATION_CHOICES)
	fm_name = forms.CharField(widget=forms.HiddenInput, initial=u'BreakForm')
