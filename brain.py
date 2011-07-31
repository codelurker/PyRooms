import var

class brain:
	def __init__(self, owner):
		self.owner = owner
		
		self.locations = []  	#dict: name:name, loc:x,y, path:[{start:startpos,path:path}]
		self.people = []		#dict: name:(fname,lname), id:id, description:physdescription
	
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

		if not self.know_person(person):
			self.add_person(person)
			person.brain.add_person(self.owner)
			
		_p = self.get_compatibility_with(person)
		
		if _p >= 20:
			_items.append({'topic':'Tell me more about yourself.','trigger':self.owner.who_am_i,'args':2})
			_items.append({'topic':'How are you feeling?'})
		
		for i in range(1,len(_items)+1):
			var._c.log('%s) %s' % (str(i),_items[i-1]['topic']))
		
		choice = int(raw_input('# '))-1
		
		while choice >= len(_items) or choice < 0:
			var._c.log('\'%s\' is not a valid topic choice.' % str(choice+1))
			choice = int(raw_input('# '))-1
		
		var._c.log('%s %s now knows %s %s.' % (self.owner.name[0],self.owner.name[1],person.name[0],person.name[1]))
		var._c.log('You: %s' % _items[choice]['topic'])
		var._c.log('%s: %s' % (self.owner.name[0],_items[choice]['trigger'](detail=_items[choice]['args'])))
		
		return len(_items)

	def know_person(self, person):
		for person in self.people:
			if person['id'] == person.id:
				return True
		
		return False
	
	def add_person(self, person):
		self.people.append({'name':person.name,'id':person.id,'obj':person})
	
