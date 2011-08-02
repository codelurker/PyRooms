import var

class brain:
	def __init__(self, owner):
		self.owner = owner
		
		self.locations = []  	#dict: name:name, loc:x,y, path:[{start:startpos,path:path}]
		self.people = []		#dict: name:(fname,lname), id:id, description:physdescription, detail:[details]
	
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