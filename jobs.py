import var, copy

class job:
	def __init__(self,name):
		var.jobs.append(self)
		self.name = name
		
		self.owner = None		
		self.schedule = []
		self.employees = []
	
	def is_qualified(self,person):
		if person.strength >= self.strength_needed and\
				person.dexterity >= self.dexterity_needed and\
				person.intelligence >= self.dexterity_needed:
					return True
	
	def hire(self,person):
		if self.is_qualified(person):
			if self.owner:
				self.employees.append(person)
				var._c.append()
			else:
				self.owner = person
			
			person.job = self
			person.job_since = list(var._c.date)
			
			return True
		else:
			return False
			
def get_job(name):
	_l = []
	
	for job in var.jobs:
		if job.name.lower() == name.lower():
			_l.append(copy.copy(job))
	
	if _l:
		return _l[0]
	else:
		var._c.log('Couldn\'t get any jobs of name %s' % name,error=1)