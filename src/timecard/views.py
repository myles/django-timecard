import datetime, time

from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
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
		manager = Employee.objects.get(manager__in=[user,])
	except Employee.DoesNotExist:
		manager = None
	
	if not manager and not employee:
		return HttpResponseForbidden()
	
	if request.method == 'POST':
		new_data = request.POST.copy()
		form = TimecardForm(new_data)
		if form.is_valid():
			try:
				timecard = Timecard.objects.get(user=user, date=datetime.date.today())
			except Timecard.DoesNotExist:
				timecard = Timecard.objects.create(user=user, date=datetime.date.today(), time_in=form.cleaned_data['time_in'])
			
			timecard.time_in = form.cleaned_data['time_in']
			timecard.time_out = form.cleaned_data['time_out']
			timecard.lunch_out = form.cleaned_data['lunch_out']
			timecard.lunch_in = form.cleaned_data['lunch_in']
			timecard.save()
			
			if timecard.time_in:
				return HttpResponseRedirect(timecard.get_absolute_url())
			else:
				return HttpResponseRedirect(reverse('timecard_homepage'))
		else:
			return HttpResponseRedirect(reverse('timecard_homepage') + "?status=failure")
	
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
				'lunch_out': timecard.lunch_out,
				'lunch_in': timecard.lunch_in,
			})
		except Timecard.DoesNotExist:
			timecard = None
			form = TimecardForm(initial={
				'date': datetime.date.today(),
			})
		
		context['timecard'] = timecard
		context['form'] = form
	
	return render_to_response('timecard/index.html', context, context_instance=RequestContext(request))

def weekly(request, username, year, week):
	user = request.user
	
	try:
		employee = Employee.objects.get(employee__username=username)
	except Employee.DoesNotExist:
		raise Http404
	
	if not user.has_perm('add_timecard') or not user.has_perm('edit_timecard'):
		return HttpResponseForbidden()
	
	try:
		manager = Employee.objects.get(employee=employee.employee, manager__in=[request.user,])
	except Employee.DoesNotExist:
		manager = None
		employee = Employee.objects.get(employee=user)
		
		if not user == employee.employee:
			return HttpResponseForbidden()
	
	try:
		date = datetime.date(*time.strptime(year + '-0-' + week, '%Y-%w-%U')[:3])
	except ValueError:
		raise Http404
	
	first_date = date
	last_date = date + datetime.timedelta(days=7)
	
	queryset = Timecard.objects.filter(user=employee.employee, date__gte=first_date, date__lt=last_date).order_by('date')
	
	week_total_hours = 0
	for timecard in queryset:
		week_total_hours = week_total_hours + timecard.hours
	
	context = {
		'employee': employee,
		'manager': manager,
		'timecards': queryset,
		'first_date': first_date,
		'last_date': last_date,
		'week_total_hours': week_total_hours
	}
	
	return render_to_response('timecard/weekly.html', context, context_instance=RequestContext(request))