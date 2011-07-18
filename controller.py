#!/usr/bin/python2
import functions, people, var, words
import items as item

class room:
	def __init__(self):
		self.name = 'The TesterToaster House'
		self.on_enter = ''
		self.description = ''
		self.built_with = 'stone'
		
		self.objects = []
		self.guests = []
	
	def add_object(self,obj,place=None):
		if not place:
			obj.location = words.get_desc_random_location()
		self.objects.append(obj)

	def add_guest(self,person):
		self.guests.append(person)
	
	def parse_room(self,detail=True):
		_lights = 0
		
		for obj in self.objects:
			if obj.type == 'light':
				_lights += 1
		
		self.on_enter += words.get_desc_lighting(_lights,detail)
		if detail: self.on_enter += ' '+words.get_desc_interior(self.built_with)
		
		for obj in self.objects:
			self.description += ' '+obj.get_room_description()
			if detail: self.description += ' '+obj.get_description()
		
		for per in self.guests:
			self.description += ' %s is here.' % (per.name[0])
	
	def get_description(self):
		self.parse_room()
		
		return '%s%s' % (self.on_enter,self.description)

class controller:
	def __init__(self,size=(32,32)):
		self.map = []
		self.size = size
		self.date = [1,0]
		self.ticks = 0
		self.people = []
		
	def generate(self):
		if var.debug: print 'Making world',
	
		for x in range(self.size[0]):
			if var.debug: print '.',
			ycols = []
			
			for y in range(self.size[1]-1):
				_r = room()
				_r.add_object(item.get_item('light'))
				ycols.append(_r)
			
			self.map.append(ycols)
		
		if var.debug: print 'Done!\n',
	
	def make_human_race(self):
		adam = people.human()
		adam.name = ['Adam',functions.get_last_name(adam.race)]
		adam.age = 30
		adam.strength = 6
		adam.dexterity = 4
		adam.intelligence = 6
		adam.charisma = 6
		
		eve = people.human()
		eve.name = ['Eve',functions.get_last_name(adam.race)]
		eve.male = False
		eve.age = 25
		eve.strength = 4
		eve.dexterity = 5
		eve.intelligence = 3
		eve.charisma = 8
		
		adam.marry(eve)
		adam.warp_to([0,0])
		eve.warp_to([0,0])
		
		for _r in range(2,people.random.randint(4,5)):
			eve.impregnate(adam)
		
	def tick(self,ticks = 1):
		print 'Ticking',
		
		for _t in range(ticks):
			print '.',
			self.ticks += _t
			
			if self.ticks == 1440:
				self.date[1]+=1
				self.ticks = 0
		
		print 'Done!\n',
	
	def tick_year(self,amnt):
		if amnt == 1:
			print '[Time] Advancing 1 year.'
		else:
			print '[Time] Advancing %s years.' % amnt
		
		for _y in range(14400*amnt):
			for _p in self.people:
				_p.tick()
			
			self.ticks += 1
			
			if self.ticks/48 > self.date[0]:
				self.date[0]+=1
			
			if self.ticks == 14400:
				self.date[0]=1
				self.date[1]+=1
				self.ticks = 0
				
				#print '[Time] It is now year %s.' % self.date[1]
				
				for _p in self.people:
					_p.events['lastbirthday']=False