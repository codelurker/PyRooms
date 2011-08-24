#!/usr/bin/python2
import random, functions, brain, words, ai, var
import items as item

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
		self.room_loc = [2,2]
		self.birthplace = self.get_room()
		self.in_room = False
		self.in_dungeon = False
		self.move_ticks = 0
		self.room_move_ticks = 0
		self.action = None
		self.attacking = False
		
		self.likes = ['price','damage','defense']
		self.needs = ['rest']
		
		self.bleeding = {'head':0,'eyes':0,\
						'larm':0,'rarm':0,\
						'lhand':0,'rhand':0,\
						'chest':0,'stomach':0,\
						'torso':0,'groin':0,\
						'lleg':0,'rleg':0,\
						'lfoot':0,'rfoot':0}		
		self.condition = {'head':10,'eyes':10,\
						'larm':10,'rarm':10,\
						'lhand':10,'rhand':10,\
						'chest':10,'stomach':10,\
						'torso':10,'groin':10,\
						'lleg':10,'rleg':10,\
						'lfoot':10,'rfoot':10}		
		self.wearing = {'head':None,'eyes':None,\
						'larm':None,'rarm':None,\
						'lhand':None,'rhand':None,\
						'chest':None,'stomach':None,\
						'torso':None,'groin':None,\
						'lleg':None,'rleg':None,\
						'lfoot':None,'rfoot':None}	
		self.multiplier = {'head':2.0,'eyes':2.5,\
						'larm':.40,'rarm':.40,\
						'lhand':.20,'rhand':.20,\
						'chest':1.5,'stomach':1.0,\
						'torso':1.5,'groin':2.0,\
						'lleg':1.0,'rleg':1.0,\
						'lfoot':.40,'rfoot':.40}
		self.accuracy = {'head':35,'eyes':45,\
						'larm':30,'rarm':30,\
						'lhand':40,'rhand':40,\
						'chest':25,'stomach':25,\
						'torso':25,'groin':25,\
						'lleg':30,'rleg':30,\
						'lfoot':40,'rfoot':40}
		self.wielding = {'lhand':None,'rhand':None}
		self.hp = 10
		self.mhp = 10
		self.strength = 0
		self.dexterity = 0
		self.intelligence = 0
		self.charisma = 0
		self.weight = 0
		self.stamina = 10
		self.max_stamina = 10
		
		#GAHHHHHHHHHHH CHANGEEEEEEEEEEEEEE
		self.defense = 3
		
		#For self.brain...
		self.alert = 1
		self.notoriety = 0
		self.lastattacked = None

		self.potential_strength = 0
		self.potential_dexterity = 0
		self.potential_intelligence = 0
		self.potential_charisma = 0
		
		#jobs
		self.job = None
		
		#skills
		self.medicine = 5
		self.speech = 2
		self.perception = 25
		
		self.skills = {'smallblades':3,'handtohand':3,'defense':2}
		
		#attributes
		self.attributes = {'naturalbeauty':False,\
							'conartist':False}
		
		self.items = []
		self.events = {'lastbirthday':False,\
						'pregnant':False,\
						'pregnanton':False,\
						'pregnantby':None,\
						'seek_partner_age':None}
		self.schedule = []
		self.path = None
		self.history = []
		self.room_path = None
		
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
			if len(self.wearing):
				for item in self.wearing:
					if item.prefix:
						_s += ' %s ' % (item.prefix)
					else:
						_s += ' '
					
					_s += '%s %s,' % (item.madeof,item.name)
				
				_s = _s[:len(_s)-1]+_s[len(_s)-1].replace(',',', ')
			
			else:
				_s += ' nothing, '
			
			_s += 'appears to be '
			neg = -1
			if self.age <= 12:
				_s += 'very young, '
				neg = 1
			elif self.age > 12 and self.age <= 32:
				_s += 'of fair age, '
				neg = 0
				
			if self.strength >= 6:
				if neg:
					_s += 'yet '
				else:
					_s += 'and '
				
				_s += 'strongly built'
				neg = 0
			
			elif self.strength < 6:
				if neg:
					_s += 'and '
				else:
					_s += 'but '
				
				_s += 'weak'
				neg = 1
					
		return _s
	
	def add_item(self, item):
		self.items.append(item)
	
	def wear(self, item):
		self.wearing[item.slot] = item
	
	def about_place(self, place):
		return {'text':'i dunno lol','detail':None}
	
	def who_am_i(self, detail=0):
		#Name
		_s = '%s %s %s. ' % (words.get_phrase('introduction'),self.name[0],self.name[1])
		_d = []

		if detail >= 1:
			if self.loc == self.birthplace.loc:
				_g = 'origin-local'
			else:
				_g = 'origin-foreign'
			
			_s += '%s %s. ' % (words.get_phrase(_g).replace('%direction%',self.get_room().get_direction_to(self.birthplace)), self.birthplace.name)
			_d.append('birthplace')
		
			if detail >= 2:
				_s += '%s. ' % (words.get_phrase('job').replace('%year%',str(self.job_since[1])).replace('%job%',self.job.name))
				_d.append('job')
			
		elif not detail:
			_s += '%s' % (words.get_phrase('uncomfortable'))
		
		return {'text':_s,'detail':_d}
	
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
	
	def pick_up(self):
		for item in self.get_room().objects:
			if item.room_loc == self.room_loc:
				item.take(self)
				break
	
	def enter_room(self):
		self.in_room = True
		if not len(self.get_room().map):
			self.get_room().generate()
		
		self.get_room().tick(light=False)
	
	def enter_dungeon(self,dungeon):
		var.player.in_dungeon = True
		dungeon.guests.append(self)
	
	def leave_dungeon(self,dungeon):
		var.player.in_dungeon = False
		dungeon.guests.remove(self)
	
	def say(self,text,action=False,quiet=False):
		self.history.append(text)
		
		if var.player.loc == self.loc:
			_s = ''
			
			if action and not quiet:
				_s = '%s %s' % (self.name[0],text)
			elif action and quiet:
				self.get_room().noises.append('%s %s.' % (self.name[0],text))
			elif not action and not quiet:
				_s = '%s: %s' % (self.name[0],text)
			elif not action and quiet:
				self.get_room().noises.append('%s: %s.' % (self.name[0],text))
			
			if _s:
				if not _s[len(_s)-1] in ['!','?']: _s+='.'
				var._c.log(_s)
	
	def attack(self,pos):
		for obj in self.get_room().objects:
			if obj.room_loc == pos:
				if not self.wielding['lhand'] and not self.wielding['rhand']:
					if var.player == self:
						var._c.log('You punch the %s.' % obj.name)
						obj.attacked(self,'lhand')
						self.attacking = False
						return True
				
				else:
					if var.player == self:
						var._c.log('You stab the %s.' % obj.name)
						for hand in self.wielding.iterkeys():
							if self.wielding[hand]:
								obj.attacked(self,self.wielding[hand])
								self.attacking = False
								return True
		
		for guest in self.get_room().guests:
			if guest.room_loc == pos:
				if not self.wielding['lhand'] and not self.wielding['rhand']:
					if var.player == self:
						guest.attacked(self,'head','lhand')
						self.lastattacked = guest
						self.notoriety = 1
					else:
						if guest == var.player:
							self.lastattacked = guest
							guest.attacked(self,'head','lhand')
						else:
							self.lastattacked = guest
							guest.attacked(self,'head','lhand')
						
						return True
				
				else:
					if var.player == self:
						for hand in self.wielding.iterkeys():
							if self.wielding[hand]:
								guest.attacked(self,'head',self.wielding[hand],hand=hand)
								self.lastattacked = guest
								self.notoriety = 1
		
		self.attacking = False
	
	def attacked(self,by,to,wep,hand=None):
		ar = by.strength / 4
		dr = 0
		
		#Add bonuses based on weapon type
		#While we're here, calculate damage
		if wep in ['lhand','rhand']:
			action = 'punch'
			ar += by.skills['handtohand']
			dam = functions.roll(1,by.skills['handtohand'])
			
			dr += by.skills['handtohand']
		elif wep.category in ['knife','ssword']:
			action = 'stab'
			ar += by.skills['smallblades']
			ar += wep.attack
			dam = functions.roll(1,by.skills['smallblades'])
			dam += functions.roll(1,wep.attack)
			if hand:
				handcon = (10-by.condition[hand[0]+'arm'])
				armcon = (10-by.condition[hand])
				
				if armcon:
					var._c.log('Your %s hurts.' % words.translate[hand])
				if handcon:
					var._c.log('Your %s hurts.' % (words.translate[hand[0]+'arm']))
				
				dam -= armcon				
		
		#Find defense rating
		if self.alert: dr += self.defense * 4
		
		#Random number + roll
		n = random.randint(1,100)
		
		if ar+n > dr or self.alert == False:
			#Did we hit the target area?
			roll = random.randint(1,50)

			if roll >= self.accuracy[to]:
				pass
			else:
				_acc = dict(self.accuracy)
				del _acc[to]
				to = random.choice([a for a in _acc.iterkeys()])
			
			#Subtract damage from armor
			if self.wearing[to]:
				dam -= functions.roll(1,self.wearing[to].defense - ((self.wearing[to].defense/2)*(not self.alert)))
			
			#Correct damage
			if dam <= 0:
				if by == var.player:
					var._c.log('%s\'s %s absorbs your hit.' % (self.name[0],self.wearing[to].name))
				#else:
				#	var._c.log('You are unharmed.')
				
				return False
			
			if by == var.player:
				_dam = dam*float(self.multiplier[to])
				var._c.log('You %s %s in the %s for %s damage.' % (action,self.name[0],words.translate[to],_dam))
				self.condition[to] -= dam
				self.hp -= _dam
			else:
				_dam = dam*float(self.multiplier[to])
				by.say('%ses you in the %s for %s damage' % (action,words.translate[to],_dam),action=True)
				self.condition[to] -= dam
				self.hp -= _dam
		else:
			if self == var.player:
				var._c.log('You block %s\'s punch' % by.name[0])
			else:
				self.say('blocks your punch',action=True)
	
	def walk(self,dir):
		if self.in_room:# or (var.player.in_room and self.loc == var.player.loc):
			_tloc = list(self.room_loc)
		else:
			try:
				var._c.map[self.loc[0]][self.loc[1]].guests.remove(self)
			except:
				var._c.log('Guest remove for %s failed with ID[%s].' % (self.get_room().name, self.id), error=True)
				
			_tloc = list(self.loc)
		
		if dir == 'north':
			_tloc[1] -= 1
		elif dir == 'south':
			_tloc[1] += 1
		elif dir == 'east':
			_tloc[0] += 1
		elif dir == 'west':
			_tloc[0] -= 1
		
		if _tloc[0] < var.world_size[0] and _tloc[1] < var.world_size[1] and var._c.map[_tloc[0]][_tloc[1]] or self.in_room == True:
			if self.in_room:# and not self.in_dungeon or (var.player.in_room and self.loc == var.player.loc and not var.player.in_dungeon):
				if _tloc[0] < 0:
					var._c.map[self.loc[0]][self.loc[1]].guests.remove(self)
					self.loc[0]-=1
					self.room_loc[0] = var.room_size[0]-1
					
					var._c.map[self.loc[0]][self.loc[1]].guests.append(self)
					self.enter_room()
					
				elif _tloc[0] == var.room_size[0]:
					var._c.map[self.loc[0]][self.loc[1]].guests.remove(self)
					self.loc[0]+=1
					self.room_loc[0] = 0
					
					var._c.map[self.loc[0]][self.loc[1]].guests.append(self)
					self.enter_room()
				
				elif _tloc[1] == 0:
					var._c.map[self.loc[0]][self.loc[1]].guests.remove(self)
					self.loc[1]-=1
					self.room_loc[1] = var.room_size[1]-1
					
					var._c.map[self.loc[0]][self.loc[1]].guests.append(self)
					self.enter_room()
				
				elif _tloc[1] == var.room_size[1]:
					var._c.map[self.loc[0]][self.loc[1]].guests.remove(self)
					self.loc[1]+=1
					self.room_loc[1] = 1
					
					var._c.map[self.loc[0]][self.loc[1]].guests.append(self)
					self.enter_room()
				
				else:
					if self.get_room().map[_tloc[0]][_tloc[1]] == 'wall':
						if self == var.player:
							var._c.status('There is a wall in the way.')
						else:
							self.say('runs into a wall',action=True,quiet=True)
					else:
						if self.attacking:
							self.attack(_tloc)
						else:
							for obj in self.get_room().objects:
								if obj.room_loc == [_tloc[0],_tloc[1]] and obj.blocking:
									if self == var.player:
										var._c.status('There is a %s in the way.' % obj.name)
									else:
										self.say('runs into a %s' % obj.name,action=True,quiet=True)
									
									return False
						
							self.room_loc = _tloc
						
						if self == var.player:
							for i in self.items:
								i.room_loc = self.room_loc
							
							var.window.clear('status')
							var.window.refresh('status')
							
							for o in self.get_room().objects:
								if o.room_loc == self.room_loc:
									var.window.write('status','You see a %s here.' % (o.name),(0,1))
									var.window.refresh('status')
			
			elif self.in_dungeon:
				self.room_loc = _tloc
			
			else:
				self.loc = _tloc
				var._c.map[_tloc[0]][_tloc[1]].guests.append(self)
			
			#if not self == var.player: var._c.log(self.parse(words.get_phrase('room_exit'),search={'find':'%direction%','replace':dir}))			
			if var.debug: var._c.log('Moving %s, %s,%s' % (dir,str(self.loc[0]),str(self.loc[1])))
		else:
			if self == var.player:
				var._c.log('There is nothing in that direction.')
	
	def get_walk_dir(self, npos, room=False):
		if room:
			if npos[0]-self.room_loc[0] == -1:
				return 'west'
			elif npos[0]-self.room_loc[0] == 1:
				return 'east'
			elif npos[1]-self.room_loc[1] == -1:
				return 'north'
			elif npos[1]-self.room_loc[1] == 1:
				return 'south'
		else:
			if npos[0]-self.loc[0] == -1:
				return 'west'
			elif npos[0]-self.loc[0] == 1:
				return 'east'
			elif npos[1]-self.loc[1] == -1:
				return 'north'
			elif npos[1]-self.loc[1] == 1:
				return 'south'
	
	def walk_to(self, to):
		p = ai.AStar(self.loc,to,avoidType='lake')
		self.path = p.getPath()
	
	def walk_to_room(self, to):
		if var.debug: var._c.log('Going from %s,%s to %s,%s' % (self.room_loc[0],self.room_loc[1],to[0],to[1]))
		
		_avoid = []
		for item in self.get_room().objects:
			if item.blocking:
				_avoid.append(item.room_loc)
		
		p = ai.AStar(self.room_loc,to,self.get_room().map,room=True,size=var.room_size,avoidType='wall',avoidArray=_avoid)
		self.path = p.getPath()
		
	def warp_to(self,place):
		self.loc = place
		var._c.map[place[0]][place[1]].add_guest(self)
	
	def get_room(self):
		return var._c.map[self.loc[0]][self.loc[1]]
	
	def get_dist_to(self,pos):
		return (abs(self.room_loc[0]-pos[0])+abs(self.room_loc[1]-pos[1]))+1
	
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

		#var._c.log('%s %s %s has married %s %s' % (var._c.date,self.name[0],self.name[1],_spouse.name[0],_spouse.maiden_name))
		pass
	
	def impregnate(self,male):
		if self.male and var.debug: print 'What are you doing?'
		if self.events['pregnant'] == True: return 0
		
		self.events['pregnant'] = True
		self.events['pregnanton'] = var._c.date #tuple(var._c.date)
		self.events['pregnantby'] = male
		
		_f_date = functions.get_future_date(9600)
		self.schedule_add(_f_date,self.have_child,args=male)
		
		#var._c.log('%s %s %s is pregnant.' % (self.events['pregnanton'],self.name[0],self.name[1]))
		pass
	
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
		
		#var._c.log('%s %s %s has been born.' % (functions.get_date(),_child.name[0],_child.name[1]))
		pass
	
	def examine_inventory(self):
		for i in self.items:
			if i.type == 'weapon' and i.wielding == False:
				for hand in self.wielding.iterkeys():
					if not self.wielding[hand] and i.wielding == False:
						self.wielding[hand] = i
						i.wielding = True
						self.say('equips a %s' % i.name,action=True)

	def check_body_parts(self):
		for part in words.body_parts:
			if part == 'head':
				if self.condition[part] <= 3 and self.alert:
					self.alert = 0
					self.say('passes out',action=True)
				elif self.condition[part] <= 0:
					self.say('dies from a severe head wound',action=True)
					self.kill()
					return False
			elif part == 'eyes':
				if self == var.player:
					if self.condition[part] <= 9:
						var._c.log('You have trouble seeing the world around you.')
		
		if self.hp <= 0:
			self.say('dies',action=True)
			self.kill()
			return False
		
		return True
	
	def player_tick(self):
		#Health
		health = []
		
		_t = 0
		for part in words.body_parts:
			_t += self.condition[part]
		
		health.append('Condition:')
		health.append('%s/%s' % (_t,140))
		
		for bodypart in self.bleeding.iterkeys():
			if self.bleeding[bodypart]:
				self.condition[bodypart]-=1
				self.bleeding[bodypart]-=1
				
				if not self.bleeding[bodypart]:
					var._c.log('Your %s stops bleeding.' % (words.translate[bodypart]))
				else:
					health.append(' ')
					health.append('Bleeding.')
		
		health.append(' ')
		health.append('Time:')
		health.append('%s:%s:%s' % (var._c.time[0],var._c.time[1],var._c.time[2]))
		health.append(' ')
		health.append('STA:')
		health.append(str(self.stamina))
		
		if self.in_room or self.in_dungeon:	
			var.window.clear('health')
			var.window.write('health',' '.join(health),(0,1))
			var.window.refresh('health')

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
		
		if self.action:
			if self.action == 'rest':
				if self.stamina < self.max_stamina:
					self.stamina += 1
					self.alert = 0
					self.say('snores',action=True,quiet=True)
				
				else:
					self.action = None
					self.brain.need = {'value':0,'obj':None}
					self.alert = 1

		if not self.check_body_parts(): return 0
		
		if self.alert:
			self.brain.think()
			self.examine_inventory()
		
		for i in self.items:
			i.room_loc = self.room_loc
		
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
			if self.in_room:# and self.loc == var.player.loc:
				if self.room_move_ticks == 0:
					_p = self.path.pop()
					_w = self.get_walk_dir(_p,room=True)
					self.walk(_w)
					self.room_move_ticks = var.room_move_ticks
				else:
					self.room_move_ticks -= 1				
			else:
				if self.move_ticks == 0:
					self.walk(self.get_walk_dir(self.path.pop()))
					self.move_ticks = var.move_ticks
				else:
					self.move_ticks -= 1
	
	def kill(self):
		c = item.corpse(self.name,self.loc,self.room_loc)
		self.get_room().add_object(c)
		
		var._c.log('You feel a life pass from this world.')
		self.get_room().guests.remove(self)
		var._c.people.remove(self)

class human(person):
	def __init__(self,player=False):
		person.__init__(self,player=player)
		
		self.race = 'Human'