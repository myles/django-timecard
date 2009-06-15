import datetime

from dateutil import parser

from django import forms

class TimeWidget(forms.widgets.Input):
	format = '%I:%M %p' # '12:20 pm'
	
	def __init__(self, attrs=None, format=None):
		self.attrs = {'class': 'vTimeField', 'size': '8', 'autocomplete': 'off'}
		super(TimeWidget, self).__init__(self.attrs)
		if format:
			self.format = format
	
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		elif hasattr(value, 'strftime'):
			value = parser.parse(value)
		
		return super(TimeWidget, self).render(name, value, attrs)

class FuzzyTimeField(forms.Field):
	def clean(self, value):
		super(FuzzyTimeField, self).clean(value)
		if value in (None, ''):
			return None
		if isinstance(value, datetime.time):
			return value
		try:
			return parser.parse(value).time()
		except ValueError, e:
			raise ValidationError(u'Enter a valid date and time')

class TimecardForm(forms.Form):
	date = forms.DateField(label=u'Date', widget=forms.HiddenInput)
	time_in = FuzzyTimeField(label=u'Time in', required=True, widget=TimeWidget)
	lunch_out = FuzzyTimeField(label=u'Lunch out', required=False, widget=TimeWidget)
	lunch_in = FuzzyTimeField(label=u'Lunch in', required=False, widget=TimeWidget)
	time_out = FuzzyTimeField(label=u'Time out', required=False, widget=TimeWidget)