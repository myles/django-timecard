from django.db.models import Manager

class EntryManager(Manager):
	
	def total_day(self, day, user):
		total = float(0)
		
		for e in self.get_query_set().filter(date=day, user=user):
			total += e.difference
		
		return total
	
	def total_between(self, start_date, end_date, user):
		total = float(0)
		
		entries = self.get_query_set().filter(date__range=(start_date, end_date), user=user)
		for e in entries:
			total += e.difference
		
		return total