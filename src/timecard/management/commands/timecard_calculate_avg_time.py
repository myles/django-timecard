import datetime, logging, optparse

from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = "Calculates the average time an employee clock's in and out."
	
	def handle(self, *args, **options):
		from timecard.models import Timecard, Employee
		
		try:
			from django.db.models import Avg
		except ImportError:
			print "Upgrade to Django 1.1"
			return 0
		
		employees = Employee.objects.all()
		
		for employee in employees:
			time_avg = Timecard.objects.filter(
				user=employee.employee).aggregate(Avg('time_in'), Avg('time_out'))
			
			if time_avg['time_in__avg']:
				employee.avg_time_in = datetime.time(int(time_avg['time_in__avg']))
			
			if time_avg['time_out__avg']:
				employee.avg_time_out = datetime.time(int(time_avg['time_out__avg']))
			
			employee.save()