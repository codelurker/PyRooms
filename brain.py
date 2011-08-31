import var, ai

class brain:
	def __init__(self, owner):
		self.owner = owner
		
		self.locations = []  	#dict: name:name, loc:x,y, path:[{start:startpos,path:path}]
		self.people = []		#dict: name:(fname,lname), id:id, description:physdescription, detail:[details]
		
		self.base = 'instinct'
		
		self.want = {'value':0,'obj':None}
		self.need = {'value':0,'obj':None}
		self.focus = None
		self.love = {'value':0,'obj':None}
		self.hate = {'value':0,'obj':None}
		self.lhate = None
	
	def get_compatibility_with(self, person):
		_p = 0 #how comfortable this person is with talking to <person>
		
		if person.get_health() == 'good': _p += 10
		
		if self.owner.race == person.race:
			if self.owner.male == person.male:
				_p += 10
			else:
				_p += 5
		else:
			if self.owner.male == person.male:
				_p -= 5
			else:
				_p -= 10
		
		#Add in <person>'s charisma
		_char_bonus = 0
		
		if self.owner.race == person.race:
			if self.owner.male:
				if person.male:
					_char = (person.charisma / 2)
					_p += _char
					_char_bonus += _char
				else:
					_char = person.charisma
					_p += person.charisma
					_char_bonus += _char					
			else:
				if person.male:
					_char = person.charisma
					_p += person.charisma
					_char_bonus += _char	
				else:
					_char = (person.charisma / 2)
					_p += _char
					_char_bonus += _char
		else:
			if person.race == 'Elf':
				if self.owner.male:
					if person.male:
						_char = (person.charisma / 4)
						_p += _char
						_char_bonus += _char
					else:
						_char = (person.charisma / 2)
						_p += _char
						_char_bonus += _char
				else:
					if person.male:
						_char = (person.charisma / 2)
						_p += _char
						_char_bonus += _char
					else:
						_char = (person.charisma / 4)
						_p += _char
						_char_bonus += _char
		
		var._c.log('+%s Charisma bonus.' % _char_bonus)
		
		return _p

	def get_dialog_options(self, person):
		_items = []
			
		_p = self.get_compatibility_with(person)
		
		if _p >= 20:
			_items.append({'topic':'Tell me more about yourself.','trigger':self.owner.who_am_i,'args':2})
			_items.append({'topic':'How are you feeling?','trigger':self.owner.name[0],'args':None})
			
			for detail in person.brain.get_person_details(self):
				if detail == 'birthplace':
					_items.append({'topic':'Can you tell me more about %s?' % (self.owner.birthplace.name),'trigger':self.owner.about_place,'args':self.owner.birthplace.loc})
			
			_items.append({'topic':'That\'s all.','trigger':None,'args':'done'})			
		
		self.parse_dialog(_items, person)
		
	def parse_dialog(self, _items, person):
		done = False
		if not self.know_person(person):
			self.add_person(person)
			person.brain.add_person(self.owner)
			#var._c.log('%s %s now knows %s %s.' % (self.owner.name[0],self.owner.name[1],person.name[0],person.name[1]))
			var._c.log('You now know %s %s.' % (self.owner.name[0],self.owner.name[1]))
			
		var._c.log('')
		for i in range(1,len(_items)+1):
			var._c.log('%s) %s' % (str(i),_items[i-1]['topic']))
			
		try:
			choice = int(raw_input('# '))-1
		except:
			done = True
		
		if not done:
			while choice >= len(_items) or choice < 0:
				var._c.log('\'%s\' is not a valid topic choice.' % str(choice+1))
				choice = int(raw_input('# '))-1
			
			var._c.log('You: %s' % _items[choice]['topic'])
			if _items[choice]['args'] and not _items[choice]['args'] == 'done':
				_re = _items[choice]['trigger'](_items[choice]['args'])
				var._c.log('%s: %s' % (self.owner.name[0],_re['text']))
			elif _items[choice]['args'] == 'done':
				done = True
			else:
				var._c.log('%s: %s' % (self.owner.name[0],_items[choice]['trigger']()))
		
		if not done:
			if _re['detail']:
				_a = []
				
				for detail in _re['detail']:
					_a.append(detail)
					#if detail == 'birthplace':
					#	_a.append({'topic':'Can you tell me more about %s?' % (self.owner.birthplace.name),'trigger':self.owner.about_place,'args':self.owner.birthplace.loc})
				
				person.brain.add_person_details(self, _a)
				
			self.get_dialog_options(person)
		else:
			pass
					
	def know_person(self, person):
		for _person in self.people:
			if _person['id'] == person.id:
				return True
		
		return False
	
	def add_person(self, person):
		self.people.append({'name':person.name,'id':person.id,'obj':person,'detail':[]})
	
	def add_person_details(self, person, details):
		for p in self.people:
			if p['id'] == person.owner.id:
				for d in details:
					if not d in p['detail']:
						p['detail'].append(d)
	
	def get_person_details(self, person):
		_d = []
		for p in self.people:
			if p['id'] == person.owner.id:
				for d in p['detail']:
					_d.append(d)
		
		return _d

	def get_item_value(self,obj):
		_w = 0
		_n = 0
		
		#Wants
		for i in range(len(self.owner.likes)):
			_w += (obj.stat[self.owner.likes[i]] * ((len(self.owner.likes)+1)-i)) * self.owner.alert
		
		#Needs
		for i in range(len(self.owner.needs)):
			if self.owner.needs[i]=='rest' and obj.name=='chair':
				if not obj.in_use and not obj.user == self.owner and not obj.owner:
					_n+= ((100 * (10-self.owner.stamina)) / self.owner.get_dist_to(obj.room_loc)) * self.owner.alert
			elif self.owner.needs[i]=='health' and obj.name.count('health'):
				_n+= ((100 * (10-self.owner.hp)) / self.owner.get_dist_to(obj.room_loc)) * self.owner.alert

		if obj.in_use and not obj.user == self.owner:
			_w = 0
			_n = 0
		
		#if _w:
		#	var._c.log(self.owner.name[0] + ': %s want value at %s' % (obj.name,_w))
		if _n:
			var._c.log(self.owner.name[0] + ': %s need value at %s' % (obj.name,_n))
		
		if _n >= _w:
			return ('needs',_n)
		else:
			return ('wants',_w)

	def get_perc_strength(self):
		_s = self.owner.strength * (self.owner.hp/float(self.owner.mhp))
		
		if _s <= 0: _s = 1
		
		return _s

	def examine_person(self,obj):
		#Temp
		_dist = abs(self.owner.room_loc[0]-obj.owner.room_loc[0])+abs(self.owner.room_loc[1]-obj.owner.room_loc[1])
		if not _dist: _dist = 1
		
		#Assuming friendly for now...
		_v = ((300 * (obj.get_perc_strength() / self.get_perc_strength())) - (obj.owner.notoriety*300)) / float(_dist)
		
		if self.owner.spouse == obj.owner:
			_v+=500
		
		if _v >= 0:
			love = _v
			hate = None
		else:
			hate = _v
			love = None
		
		if hate:
			var._c.log(self.owner.name[0] + ': hate for %s is %s' % (obj.owner.name[0],hate))
		
		if self.owner.name == "Albert":
			var._c.log(self.owner.name+'I am a dog!')
			var._c.log(str(-love))
			return [-hate,love]
		else:
			return [love,hate]

	def think(self):
		self.need = {'value':0,'obj':None}
		self.want = {'value':0,'obj':None}
		self.hate = {'value':0,'obj':None}
		#self.lhate = self.hate['obj']
		
		#Want/Need
		for o in self.owner.get_room().objects:
			if o.type == 'window': continue
			
			can_see = True
			if not self.owner.room_loc == o.room_loc:
				for pos in ai.line((self.owner.room_loc[0],self.owner.room_loc[1]),(o.room_loc[0],o.room_loc[1])).path:
					if self.owner.get_room().map[pos[0]][pos[1]] == 'wall':
						can_see = False
			
			if not can_see: break
			
			value = self.get_item_value(o)
			
			if value[0] == 'wants':
				if value[1] > self.want['value']:
					self.want = {'obj':o,'value':value[1]}
			elif value[0] == 'needs':
				if value[1] > self.need['value']:
					if self.need['obj']:
						self.need['obj'].in_use = False
						self.need['obj'].user = None
					
					self.need = {'obj':o,'value':value[1]}
		
		#Love/Hate
		for a in self.owner.get_room().guests:
			if not a == self.owner:
				_r = self.examine_person(a.brain)
				
				if _r[0] and _r[0] > self.love['value']:
					self.love = {'obj':a,'value':_r[0]}
				elif _r[1] and _r[1] < self.hate['value']:
					self.hate = {'obj':a,'value':_r[1]}
					
					if self.hate['obj'] == var.player:# and not self.lhate == self.hate['obj']:
						if not self.lhate == self.hate['obj']:
							self.owner.say('seems angered towards you',action=True)
							if self.hate['obj'].lastattacked == self.owner.spouse:

								if self.owner.spouse.male:
									self.owner.say('Get your hands off my husband!')
								else:
									self.owner.say('Get your hands off my wife!')
						
						self.lhate = self.hate['obj']
					
					elif not self.hate['obj'] == None and not self.hate['obj'] == var.player:
						self.owner.say('seems angered towards %s' % (self.hate['obj'].name[0]),action=True)
						self.lhate = self.hate['obj']
		
		if self.want['obj'] == None and self.need['obj'] == None and self.hate == None:
			#var._c.log('%s: I\'m bored...' % (self.owner.name[0]))
			return False
		
		if self.want['value'] > self.need['value'] and self.want['value'] > abs(self.hate['value']):
			#var._c.log(self.owner.name[0]+': I want that %s' % self.want['obj'].name)	
			if self.owner.room_loc[0] == self.want['obj'].room_loc[0] and self.owner.room_loc[1] == self.want['obj'].room_loc[1] and not self.want['obj'].owner:
				#var._c.log(self.owner.name[0]+': Picking up %s' % self.want['obj'].name)
				self.want['obj'].take(self.owner)
				
				self.want = {'value':0,'obj':None}
				
			else:
				if not self.owner.path or not self.owner.path[0] == self.want['obj'].room_loc:
					self.owner.walk_to_room((self.want['obj'].room_loc[0],self.want['obj'].room_loc[1]))

		elif self.want['value'] <= self.need['value'] and self.need['value'] > abs(self.hate['value']):	
			if self.owner.room_loc[0] == self.need['obj'].room_loc[0] and self.owner.room_loc[1] == self.need['obj'].room_loc[1] and not self.need['obj'].owner:
				self.need['obj'].take(self.owner)
				self.need = {'value':0,'obj':None}
			else:
				if not self.owner.path or not self.owner.path[0] == self.need['obj'].room_loc:
					self.owner.walk_to_room((self.need['obj'].room_loc[0],self.need['obj'].room_loc[1]))
		
		elif self.hate['obj']:
			#Can I fight him/her?
			if self.owner.hp >= 8:
				#Find out where he/she is
				#Check surroundings
				found = False
				for pos in [[-1,0],[1,0],[0,-1],[0,1]]:
					if [self.owner.room_loc[0]+pos[0],self.owner.room_loc[1]+pos[1]] == self.hate['obj'].room_loc:
						self.owner.attack([self.owner.room_loc[0]+pos[0],self.owner.room_loc[1]+pos[1]])
						self.owner.path = None
						found = True
				
				if not found:				
					self.owner.walk_to_room((self.hate['obj'].room_loc[0],self.hate['obj'].room_loc[1]))
			else:
				#Figure out what to do
				if not self.owner.drink_potion('health'):
					self.owner.walk_to_room((1,1))
					self.owner.say('flees in terror',action=True)
		
		#if self.love:
		#	var._c.log(self.owner.name[0]+': Love %s' % self.love['obj'].name[0])