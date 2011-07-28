#!/usr/bin/python2
import functions, people, var, words
import items as item

class room:
	def __init__(self, coords):
		self.name = 'The TesterToaster House'
		self.type = ''
		self.on_enter = ''
		self.description = ''
		self.built_with = ''
		self.coords = coords
		
		self.objects = []
		self.guests = []
				
		self.map = []
		self.exits = ['north','south','east','west']
		
		for x in range(0,var.room_size[0]):
			ycols = []
			
			for y in range(0,var.room_size[1]):
				ycols.append({'object':0})
			
			self.map.append(ycols)
	
	def get_description(self):
		self.parse_room()
		
		return '%s%s' % (self.on_enter,self.description)
	
	def get_direction_to(self, place):
		_s = ''
		
		if place.coords[0] < self.coords[0]:
			_s += 'west'
		elif place.coords[0] > self.coords[0]:
			_s += 'east'
		if place.coords[1] < self.coords[1]:
			_s = 'north' + _s
		elif place.coords[1] > self.coords[1]:
			_s = 'south' + _s
		
		return _s
	
	def add_object(self,obj,place=None):
		if not place:
			obj.location = words.get_desc_location(obj)
		self.objects.append(obj)

	def add_guest(self,person):
		self.guests.append(person)
	
	def get_lights(self):
		_lights = 0
		
		for obj in self.objects:
			if obj.type == 'light':
				_lights += 1
		
		for guest in self.guests:
			for item in guest.items:
				if item.type == 'light':
					_lights += 1
		
		return _lights
	
	def parse_room(self):
		self.on_enter = ''
		self.description = ''
		
		_lights = self.get_lights()
		
		if var.debug: print 'There are %s lights here.' % _lights
		
		_l = words.get_desc_lighting(_lights)
		if _l: self.on_enter += _l+' '
		
		self.on_enter += words.get_desc_interior(self.built_with,_lights)
		
		_objs = []
		for obj in self.objects:
			
			for _obj in _objs:
				if _obj['name'] == obj.name:
					_obj['count'] += 1
					#_obj['obj'] == obj
				else:
					_objs.append({'name':obj.name,'count':0,'obj':obj})
			
			if not len(_objs): _objs.append({'name':obj.name,'count':1,'obj':obj})
				
		_t = []
		for obj in _objs:
			if not obj['name'] in _t:
				self.description += ' '+obj['obj'].get_room_description()
				self.description += ' '+obj['obj'].get_description()
				
				if obj['count'] > 2:
					self.description += ' There are %s more %ss here.' % (obj['count']-1,obj['obj'].name)
				elif obj['count'] == 2:
					self.description += ' There is one more %s here.' % (obj['obj'].name)					
				
				_t.append(obj['name'])
		
		for per in self.guests:
			if per != var.player:
				self.description += ' %s is here.' % (per.name[0])

class controller:
	def __init__(self,size=(32,32)):
		self.map = []
		self.size = size
		self.date = [1,0]
		self.ticks = 0
		self.people = []
		self.history = []
		self.errors = []
		
		self.id = 0
	
	def log(self,text,error=False):
		if not error:
			print text
		else:
			self.errors.append(text)
		
		self.history.append(text)
		
	def get_id(self):
		self.id += 1
		return self.id
		
	def generate(self):
		if var.debug: print 'Making world',
	
		for x in range(self.size[0]):
			if var.debug: print '.',
			ycols = []
			
			for y in range(self.size[1]-1):
				if (x,y) == (0,0):
					_r = room((x,y))
					_r.type = 'home'
					_r.add_object(item.get_item('light'))
					_r.add_object(item.get_item('light'))
					_r.add_object(item.get_item('light'))
					_r.add_object(item.get_item('table'))
					_r.built_with = 'stone'
					ycols.append(_r)
				else:
					ycols.append(room((x,y)))
			
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
		
		var.player = people.human(player=True)
		var.player.name = ['Player',functions.get_last_name(adam.race)]
		var.player.male = False
		var.player.age = 25
		var.player.strength = 4
		var.player.dexterity = 5
		var.player.intelligence = 3
		var.player.charisma = 8
		var.player.birthplace = [0,1]
		
		adam.marry(eve)
		adam.warp_to([0,0])
		eve.warp_to([0,0])
		var.player.warp_to([0,0])
		#adam.walk('south')
		
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
			self.log('[Time] Advancing 1 year.')
		else:
			self.log('[Time] Advancing %s years.' % amnt)
		
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