#!/usr/bin/python2
import random, functions, brain, words, ai, var

random.seed()

class person:
	def __init__(self,player=False):
		if not player: var._c.people.append(self)
		
		self.id = var._c.get_id()		
		self.brain = brain.brain(self)
		self.name = [None,None]
		self.maiden_name = None
		self.born = tuple(var._c.date)
		self.race = None
		self.male = True
		self.age = 0
		self.parents = None
		self.spouse = None
		self.children = []
		self.siblings = []
		self.loc = [0,0]
		self.birthplace = self.get_room()
		
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
		self.weight = 0
				
		self.potential_strength = 0
		self.potential_dexterity = 0
		self.potential_intelligence = 0
		self.potential_charisma = 0
		
		#jobs
		self.occupation = 'Bum'
		self.occupation_since = [0,0]
		
		#skills
		self.medicine = 5
		self.speech = 2
		
		#attributes
		self.attributes = {'naturalbeauty':False,\
							'conartist':False}
		
		self.items = []
		self.wearing = []
		self.events = {'lastbirthday':False,\
						'pregnant':False,\
						'pregnanton':False,\
						'pregnantby':None,\
						'seek_partner_age':None}
		self.schedule = []
		self.path = None
		
		self.description = ''
	
	def get_description(self):
		pass
	
	def get_visual_description(self, short=True):
		if self.male:
			_ref = ['man','he']
		else:
			_ref = ['woman','she']
		
		_s = ''
		if short:
			_s += '%s is wearing' % (_ref[1][0].upper()+_ref[1][1:])
			for item in self.wearing:
				_s += ' %s %s %s,' % (item.prefix,item.madeof,item.name)
			
			_s = _s[:len(_s)-1]+_s[len(_s)-1].replace(',','. ')
			
			if self.strength >= 6:
				_s += '%s appears to be fairly strong.' % (_ref[1][0].upper()+_ref[1][1:])
		
		return _s
	
	def add_item(self, item):
		self.items.append(item)
	
	def wear(self, item):
		self.wearing.append(item)
	
	def who_am_i(self, detail=0):
		#Name.
		_s = '%s %s %s. ' % (words.get_phrase('introduction'),self.name[0],self.name[1])

		if detail >= 1:
			if self.loc == self.birthplace.loc:
				_g = 'origin-local'
			else:
				_g = 'origin-foreign'
			
			_s += '%s %s. ' % (words.get_phrase(_g).replace('%direction%',self.get_room().get_direction_to(self.birthplace)), self.birthplace.name)
		
			if detail >= 2:
				_s += '%s. ' % (words.get_phrase('occupation').replace('%year%',str(self.occupation_since[1])).replace('%occupation%',self.occupation))
			
		elif not detail:
			_s += '%s' % (words.get_phrase('uncomfortable'))
		
		return _s		
	
	def get_health(self):
		_t = 0
		_s = ''
		if self.male: _g = 'his'
		else: _g = 'her';
		
		for part in words.body_parts:
			_c = self.condition[part]
			_t += _c
			
		if _t >= 120:		
			return 'good'
	
	def parse(self,text,search=None):
		_t = text.replace('%name%',self.name[0]).replace('%fname%','%s %s' % (self.name[0],self.name[1]))
		
		if search: _t = _t.replace(search['find'],search['replace'])
		
		return _t
	
	def schedule_add(self,time,event,args):
		self.schedule.append({'time':time,'event':event,'args':args})
		if var.debug: print '[Schedule] Event added by %s %s.' % (self.name[0],self.name[1])
	
	def walk(self,dir):
		try:
			var._c.map[self.loc[0]][self.loc[1]].guests.remove(self)
		except:
			var._c.log('Guest remove for %s failed with AID[%s].' % (self.get_room().name, self.id), error=True)
		
		if dir == 'north':
			self.loc[1] -= 1
		elif dir == 'south':
			self.loc[1] += 1
		elif dir == 'east':
			self.loc[0] -= 1
		elif dir == 'west':
			self.loc[0] += 1
		
		var._c.map[self.loc[0]][self.loc[1]].guests.append(self)
		
		var._c.log(self.parse(words.get_phrase('room_exit'),search={'find':'%direction%','replace':dir}))		
		if var.debug: var._c.log('Moving %s, %s,%s' % (dir,str(self.loc[0]),str(self.loc[1])))
	
	def get_walk_dir(self, npos):
		if npos[0]-self.loc[0] == -1:
			return 'west'
		elif npos[0]-self.loc[0] == 1:
			return 'east'
		elif npos[1]-self.loc[1] == -1:
			return 'north'
		elif npos[1]-self.loc[1] == 1:
			return 'south'
	
	def walk_to(self, to):
		p = ai.AStar(self.loc,to)
		self.path = p.getPath()
		
	def warp_to(self,place):
		self.loc = place
		var._c.map[place[0]][place[1]].add_guest(self)
	
	def get_room(self):
		return var._c.map[self.loc[0]][self.loc[1]]
	
	def find_partner(self):
		for person in var._c.people:
			if not person.male and person.spouse == None:
				if person.age < person.events['seek_partner_age']:
					break
				
				if (person.intelligence+person.charisma) <= (self.intelligence+self.charisma):
					self.marry(person)
	
	def marry(self,_spouse):
		self.spouse = _spouse
		_spouse.spouse = self
		_spouse.maiden_name = _spouse.name[1]
		_spouse.name[1] = self.name[1]

		var._c.log('%s %s %s has married %s %s' % (var._c.date,self.name[0],self.name[1],_spouse.name[0],_spouse.maiden_name))
	
	def impregnate(self,male):
		if self.male and var.debug: print 'What are you doing?'
		if self.events['pregnant'] == True: return 0
		
		self.events['pregnant'] = True
		self.events['pregnanton'] = var._c.date #tuple(var._c.date)
		self.events['pregnantby'] = male
		
		_f_date = functions.get_future_date(9600)
		self.schedule_add(_f_date,self.have_child,args=male)
		
		var._c.log('%s %s %s is pregnant.' % (self.events['pregnanton'],self.name[0],self.name[1]))
	
	def have_child(self,male):
		_child = person()
		_child.race = male.race
	
		#if male.charisma + male.intelligence > self.charisma + self.intelligence:
		#	_child.male = True
		#else:
		#	_child.male = False
		
		_child.male = random.randint(0,1)
		
		_child.name = [functions.get_name(_child.race,_child.male),self.name[1]]
		#_child.birthplace = self.get_room()
		
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
		
		if _child.potential_strength > 4:
			_child.events['seek_partner_age'] = var.base_human_seek_partner_age-(random.randint(1,_child.potential_strength))
		elif _child.potential_strength <= 2:
			_child.events['seek_partner_age'] = var.base_human_seek_partner_age+(random.randint(1,_child.potential_strength))
		else:
			_child.events['seek_partner_age'] = var.base_human_seek_partner_age

		if self.spouse == male:
			_married_on_birth = True
		else:
			_married_on_birth = False
		
		_temp = {'child':_child,'mother':self,'father':male,'married_on_birth':_married_on_birth}
		
		self.children.append(_temp)
		male.children.append(_temp)
		
		self.events['pregnant'] = False
		
		var._c.log('%s %s %s has been born.' % (functions.get_date(),_child.name[0],_child.name[1]))
	
	def tick(self):
		if self.male:
			if self.age >= self.events['seek_partner_age'] and self.spouse == None:
				self.find_partner()
		
		else:
			if not self.spouse == None:
				#Check children for marriage... if not, make more :(
				_count = 0
				
				for child in self.children:
					_c = child['child']
					
					if _c.age < _c.events['seek_partner_age'] or not _c.spouse == None:
						_count += 1
				
				if not _count:
					self.impregnate(self.spouse)
		
		for _e in self.schedule:
			if _e['time'] == var._c.date:
				if _e['args'] == '':
					_e['event']()
				else:
					_e['event'](_e['args'])
				
				self.schedule.remove(_e)
		
		#check for birthday
		if var._c.date[0] == self.born[0] and self.events['lastbirthday'] == False:
			self.strength += random.randint(0,1)
			self.dexterity += random.randint(0,1)
			self.intelligence += random.randint(0,1)
			self.charisma += random.randint(0,1)
			
			self.age+=1
			self.events['lastbirthday'] = True
			#print '%s is now %s years old!' % (self.name,self.age)
		
		#Movements.
		if self.path:
			#print 'AStar '+str(self.path.pop())
			self.walk(self.get_walk_dir(self.path.pop()))

class human(person):
	def __init__(self,player=False):
		person.__init__(self,player=player)
		
		self.race = 'Human'