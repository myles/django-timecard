import datetime

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext

from timecard.models import Timecard, Employee
from timecard.forms import TimecardForm

def index(request):
	user = request.user
	
	if not user.has_perm('add_timecard') or not user.has_perm('edit_timecard'):
		return HttpResponseForbidden()
	
	try:
		employee = Employee.objects.get(employee=user)
	except Employee.DoesNotExist:
		employee = None
	
	try:
		manager = Employee.objects.filter(manager__in=[user,])
	except Employee.DoesNotExist:
		manager = None
	
	if not manager and not employee:
		return HttpResponseForbidden()
	
	if request.method == 'POST':
		new_data = request.POST.copy()
		# TODO Add the timecard saving crap here.
	
	context = {
		'employee': employee,
		'manager': manager,
		'date': datetime.date.today()
	}
	
	if employee:
		try:
			timecard = Timecard.objects.get(user=user, date=datetime.date.today())
			form = TimecardForm(initial={
				'date': datetime.date.today(),
				'time_in': timecard.time_in,
				'time_out': timecard.time_out,
				'lunch_in': timecard.lunch_in,
				'lunch_out': timecard.lunch_out,
			})
		except Timecard.DoesNotExist:
			timecard = None
			form = TimecardForm(initial={
				'date': datetime.date.today(),
			})
		
		context['timecard'] = timecard
		context['form'] = form
	
	return render_to_response('timecard/index.html', context, context_instance=RequestContext(request))