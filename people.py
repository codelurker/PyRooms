#!/usr/bin/python2
import random, interpreter, var

random.seed()

class person:
	def __init__(self):
		var._c.people.append(self)
		
		self.name = ('','')
		self.born = tuple(var._c.date)
		self.race = None
		self.male = True
		self.age = 0
		self.parents = None
		self.children = []
		self.siblings = []
		
		self.condition = {'head':10,'eyes':10,\
						'larm':10,'rarm':10,\
						'lhand':10,'rhand':10,\
						'chest':10,'stomach':10,\
						'torso':10,'groin':10,\
						'lleg':10,'rleg':10,\
						'lfoot':10,'rfoot':10}
		self.strength = 0
		self.dexterity = 0
		self.intelligence = 0
		self.charisma = 0
		
		self.potential_strength = 0
		self.potential_dexterity = 0
		self.potential_intelligence = 0
		self.potential_charisma = 0
		
		self.items = []
		self.events = {'lastbirthday':False}
		self.schedule = []
	
	def schedule_add(self,time,event,args=''):
		self.schedule.append({'time':time,'event':event,'args':args})
	
	def have_child(self,male):
		_child = person()
		_child.race = male.race
	
		if male.charisma + male.intelligence > self.charisma + self.intelligence:
			_child.male = True
		else:
			_child.male = False
		
		_child.name = (interpreter.get_name(_child.race,_child.male),'')
		
		_strength = sorted([self.strength,male.strength])
		_dexterity = sorted([self.dexterity,male.dexterity])
		_intelligence = sorted([self.intelligence,male.intelligence])
		_charisma = sorted([self.charisma,male.charisma])
		
		_child.potential_strength = (_strength[0]+_strength[1])/2
		_child.potential_dexterity = (_dexterity[0]+_dexterity[1])/2
		_child.potential_intelligence = (_intelligence[0]+_intelligence[1])/2
		_child.potential_charisma = (_charisma[0]+_charisma[1])/2
		
		_child.strength = random.randint(0,1)
		_child.dexterity = random.randint(0,1)
		_child.intelligence = random.randint(0,1)
		_child.charisma = random.randint(0,1)
		
		_child.parents = [male,self]
		
		print var._c.date,'CHILDZZZZZZZZZZZZ'
	
	def tick(self):
		if self.age >= 6:
			if not self.male:
				pass
			else:
				pass
		
		else:
			pass
		
		#check for scheduled events
		for _e in self.schedule:
			if _e['time'] == var._c.date:
				if _e['args'] == '':
					_e['event']()
				else:
					_e['event'](_e['args'])
				
				self.schedule.remove(_e)
		
		#check for birthday
		if var._c.date[0] == self.born[0] and self.events['lastbirthday'] == False:
			self.age+=1
			self.events['lastbirthday'] = True
			#print '%s is now %s years old!' % (self.name,self.age)


class human(person):
	def __init__(self):
		person.__init__(self)
		
		self.race = 'Human'