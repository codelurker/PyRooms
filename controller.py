#!/usr/bin/python2
import functions, people, var, ai, words, towns, random
import items as item
import jobs as job

random.seed()

class room:
	def __init__(self, loc, controller):
		self.name = 'The TesterToaster House'
		self.type = ''
		self.on_enter = ''
		self.description = ''
		self.built_with = ''
		self.loc = loc
		self.controller = controller
		
		self.objects = []
		self.guests = []
				
		self.map = []
		self.exits = []
		
		self.flags = {'sunlit':False}
		
		for x in range(0,var.room_size[0]):
			ycols = []
			
			for y in range(0,var.room_size[1]):
				ycols.append({'object':0})
			
			self.map.append(ycols)
	
	def randomize(self):
		if self.type == 'clearing':
			for n in range(0,random.randint(0,1)):
				_i = item.get_item('foliage')
				_i.loc = self.loc
				self.add_object(_i)
		
		elif self.type == 'house':
			_i = item.get_item('light')
			self.add_object(_i)
		
		elif self.type == 'forest':
			_ws = []
			for w in range(self.green/10):
				_w = ai.RandomWalker(self.loc)
				_w.walk()
				_ws.append(_w)
			
			for w in _ws:
				for _pos in w.path:
					if _pos[0]>0 and _pos[0]<var.world_size[0]-2 and _pos[1]>0 and _pos[1]<var.world_size[1]-2 and not var._c.map[_pos[0]][_pos[1]]:
						r = room(_pos,self.controller)
						r.type = 'forest'
						r.flags['sunlit'] = True
						r.green = self.green - 10
						#if r.green > 70:
						r.randomize()
						var._c.map[_pos[0]][_pos[1]] = r
						var._c.forests.append(r)
				
	def get_description(self,exits=True):
		self.parse_room(exits=exits)
		
		return self.description
	
	def get_direction_to(self, place):
		_s = ''
		
		if place.loc[0] < self.loc[0]:
			_s += 'west'
		elif place.loc[0] > self.loc[0]:
			_s += 'east'
		if place.loc[1] < self.loc[1]:
			_s = 'north' + _s
		elif place.loc[1] > self.loc[1]:
			_s = 'south' + _s
		
		return _s
	
	def find_exits(self):
		for pos in [[0,-1],[-1,0],[1,0],[0,1]]:
			if self.controller.map[self.loc[0]+pos[0]][self.loc[1]+pos[1]]:
				_r = self.controller.map[self.loc[0]+pos[0]][self.loc[1]+pos[1]]
				if pos == [0,-1]:
					self.exits.append({'dir':'north','room':_r,'window':True,'obj':None})
				elif pos == [0,1]:
					self.exits.append({'dir':'south','room':_r,'window':True,'obj':None})
				elif pos == [1,0]:
					self.exits.append({'dir':'east','room':_r,'window':True,'obj':None})
				elif pos == [-1,0]:
					self.exits.append({'dir':'west','room':_r,'window':True,'obj':None})
		
		if self.type == 'house':
			for exit in self.exits:
				#Place windows on inside.
				_i = item.get_item('window')
				_i.place = exit['dir']
				_i.inside = self
				_i.outside = exit['room']
				exit['obj'] = _i
				self.add_object(_i)
				
	def add_object(self,obj,place=None):
		obj.loc = self.loc
		if not place:
			obj.location = words.get_phrase('location')#.replace('%place%',obj.place).replace('%roomtype%',self.type)
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
	
	def parse_room(self,exits=True):
		self.description = []
		_lights = None
		
		#Lighting on the inside
		if self.type in ['house']:
			_lights = self.get_lights()
			
			if var.debug: print 'There are %s lights here.' % _lights
			
			_l = words.get_desc_lighting(_lights)
			if _l: self.description.append(_l)
			
			self.description.append(words.get_desc_interior(self.built_with,_lights))
		
		#Lighting on the outside
		if self.controller.is_daytime():
			if self.type == 'clearing':
				self.description.append(words.get_desc_outside('clearing',9))
		
		if _lights or (not self.type in ['house'] and self.controller.is_daytime()):
			#Count objects
			_objs = []
			for obj in self.objects:
				for _obj in _objs:
					if _obj['name'] == obj.name:
						_obj['count'] += 1
						
					else:
						_objs.append({'name':obj.name,'count':0,'obj':obj})
				
				if not len(_objs): _objs.append({'name':obj.name,'count':1,'obj':obj})
					
			_t = []
			for obj in _objs:
				if not obj['name'] in _t and not obj['obj'].type == 'window':
					self.description.append(obj['obj'].get_room_description())
					
					if not obj['obj'].type in ['foliage','window']:
						if obj['count'] > 2:
							self.description.append('There are %s more %ss here' % (obj['count']-1,obj['obj'].name))
						elif obj['count'] == 2:
							self.description.append('There is one more %s here' % (obj['obj'].name))
					
					_t.append(obj['name'])
			
			if exits:
				if self.type in ['house']:
					_win = 'There are windows facing '
					
					for obj in self.objects:
						if obj.type == 'window' and obj.place:
							_win += '%s, ' % (obj.place)
								
					_win = _win.split(' ')
					_win[len(_win)-3] += ' and'
					_win = ' '.join(_win)
					
					self.description.append(_win.rstrip('., '))
				else:
					for exit in self.exits:
						_exits = []
						
						for _exit in exit['room'].exits:
							if _exit['room'] == self:
								if exit['room'].type == 'house':
									_exits.append(exit)
						
						self.description.append(words.get_phrase('room_location').replace('%direction%',exit['dir']).replace('%roomtype%',exit['room'].type))
												
						for _exit in _exits:
							_ls = _exit['room'].get_lights()
							
							if _ls == 1:
								self.description.append(words.get_phrase('lightinwindowdim').replace('%direction%',words.opposite(_exit['dir'])).replace('%roomtype%',_exit['room'].type))
			
			for per in self.guests:
				if per != var.player:
					if var.player.brain.know_person(per):
						self.description.append('%s is here.' % (per.name[0]))
					else:
						if per.male:
							_ref = ['man','he']
						else:
							_ref = ['woman','she']
						
						self.description.append('A %s is here. ' % (_ref[0])+per.get_visual_description())
			
		if None in self.description:
			self.description.remove(None)
			
		self.description = '. '.join(self.description)+'.'

class controller:
	def __init__(self):
		self.map = []
		self.date = [1,0]
		self.ticks = 0
		self.history = []
		self.errors = []
		
		self.id = 0
		self.people = []
		self.jobs = []
	
	def log(self,text,error=False):
		if not error:
			if len(text)>79:
				var.window.clear('log')
				#var.window.write('log',text,(0,4-len(text)/79))
				var.window.write('log',text,(0,var.window.get_height('log')-len(text)/79))
				var.window.refresh('log')
			else:
				var.window.write_append('log',text)
				var.window.refresh('log')
			
			var.window.refresh('main')
		else:
			self.errors.append(text)
		
		self.history.append(text)
		
	def get_random_town(self):
		_t = self.towns[random.randint(0,len(self.towns)-1)]
		for pos in _t.map:
			if self.map[pos[0]][pos[1]].type == 'house':
				_h = self.map[pos[0]][pos[1]]
		
		return _h
	
	def get_id(self):
		self.id += 1
		return self.id
		
	def path_maker(self,towns):
		path = []
		
		for l in range(0,len(towns)-1):
			p = ai.AStar([towns[l].loc[0]+(towns[l].size[0]/2),towns[l].loc[1]+(towns[l].size[1]/2)],(towns[l+1].loc[0]+(towns[l+1].size[0]/2),towns[l+1].loc[1]+(towns[l+1]\
					.size[1]/2)),ignoreNone=True)
			path.extend(p.getPath())
		
		for pos in path:
			if self.map[pos[0]][pos[1]] == None:
				self.build_road(pos)
	
	def generate(self):
		#Make a blank map
		for x in range(var.world_size[0]):
			if var.debug: print '.',
			ycols = []
			
			for y in range(var.world_size[1]):
				ycols.append(None)
			
			self.map.append(ycols)
		
		#Find some spots to place towns
		self.towns = []
		for t in range(0,var.towns):
			tspot = None
			
			while tspot == None:
				_tspot = (random.randint(0,var.world_size[0]),random.randint(0,var.world_size[1]))
				if _tspot[0] > 0 and _tspot[0]+4 < var.world_size[0] and _tspot[1] > 0 and _tspot[1]+4 < var.world_size[1]:
					
					#Do they overlap?
					overlap = False
					
					for x in range(0,4):
						for y in range(0,4):
							if self.map[_tspot[0]+x][_tspot[1]+y]:
								overlap = True
								if var.debug: print 'Overlapping towns found at %s,%s. Trying again.' % (_tspot[0]+x,_tspot[1]+y)
					
					if not overlap:
						tspot = _tspot
						if var.debug: print 'Town location found: %s,%s' % (tspot[0],tspot[1])
			
			spots = []
			for x in range(0,4):
				for y in range(0,4):
					spots.append((tspot[0]+x,tspot[1]+y))# = self.build_clearing(tspot[0]+x,tspot[1]+y)
			
			_t = towns.town(tspot,spots,self)
			_t.generate()
			self.towns.append(_t)
		
		#Connect towns
		self.path_maker(self.towns)

		#Create biomes
		#Forests
		self.forests = []
		for _f in range(4):
			self.build_forest((random.randint(1,var.world_size[0]-2),random.randint(1,var.world_size[1]-2)))
		
		#Dither our forests
		for forest in self.forests:
			pass
		
		#Finish up by finding room exits
		l = None
		for x in range(var.world_size[0]):
			for y in range(var.world_size[1]):
				if self.map[x][y]:
					self.map[x][y].find_exits()
					l = self.map[x][y]
	
	def build_clearing(self,pos):
		r = room(pos,self)
		r.type = 'clearing'
		r.flags['sunlit'] = True
		r.randomize()
		
		self.map[pos[0]][pos[1]] = r
	
	def build_forest(self,pos):
		r = room(pos,self)
		r.type = 'forest'
		r.flags['sunlit'] = True
		r.green = 40
		r.randomize()

		self.map[pos[0]][pos[1]] = r
	
	def build_road(self,pos):
		r = room(pos,self)
		r.type = 'road'
		r.flags['sunlit'] = True
		
		self.map[pos[0]][pos[1]] = r
	
	def build_house(self,pos):
		r = room(pos,self)
		r.type = 'house'
		r.randomize()
		
		self.map[pos[0]][pos[1]] = r
	
	def add_job(self,job):
		self.jobs.append(job)
	
	def make_human_race(self):
		adam = people.human()
		adam.name = ['Adam',functions.get_last_name(adam.race)]
		adam.age = 30
		adam.strength = 6
		adam.dexterity = 4
		adam.intelligence = 6
		adam.charisma = 6
		adam.add_item(item.get_item_clothing('chest'))
		adam.wear(adam.items[0])
		adam.add_item(item.get_item_clothing('feet'))
		adam.wear(adam.items[1])
		
		eve = people.human()
		eve.name = ['Eve',functions.get_last_name(adam.race)]
		eve.male = False
		eve.age = 25
		eve.strength = 4
		eve.dexterity = 5
		eve.intelligence = 3
		eve.charisma = 8
		eve.add_item(item.get_item('clothing'))
		eve.wear(adam.items[0])
		
		var.player = people.human(player=True)
		var.player.name = ['Player',functions.get_last_name(adam.race)]
		var.player.male = False
		var.player.age = 25
		var.player.strength = 4
		var.player.dexterity = 5
		var.player.intelligence = 3
		var.player.charisma = 8
		
		adam.marry(eve)
		_t = self.get_random_town()
		adam.warp_to(_t.loc)
		adam.birthplace = _t
		eve.warp_to(_t.loc)
		eve.birthplace = _t
		var.player.warp_to(_t.loc)
		var.player.birthplace = var.player
		var.camera[1] = var.player.loc[1]/2
		
		self.jobs.append(job.get_job('carpenter'))
		self.jobs[0].hire(adam)
		
		for _r in range(2,people.random.randint(4,5)):
			eve.impregnate(adam)
		
	def is_daytime(self):
		return True
	
	def tick(self,ticks=1):
		if var.debug: print 'Ticking',
		
		for _t in range(ticks):
			if var.debug: print '.',
			
			for _p in self.people:
				_p.tick()
			
			self.ticks += _t
			
			if self.ticks == 14400:
				self.date[0]=1
				self.date[1]+=1
				self.ticks = 0
				
				if var.debug: print '[Time] It is now year %s.' % self.date[1]
				
				for _p in self.people:
					_p.events['lastbirthday']=False
		
		var.camera[1] = var.player.loc[1]-12
		self.draw_map()
		if var.debug: print 'Done!\n',
	
	def tick_year(self,amnt):
		if amnt == 1:
			pass
			#self.log('[Time] Advancing 1 year.')
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
	
	def draw_map(self):
		for y in range(var.world_size[1]):
			for x in range(var.world_size[0]):
				if self.map[x][y] and not (x,y) == tuple(var.player.loc):
					if self.map[x][y].type == 'house':
						var.window.write('main','H',(x-var.camera[0],y-var.camera[1]))
					elif self.map[x][y].type == 'clearing':
						var.window.write('main','.',(x-var.camera[0],y-var.camera[1]))
					elif self.map[x][y].type == 'road':
						var.window.write('main','#',(x-var.camera[0],y-var.camera[1]))
					elif self.map[x][y].type == 'forest':
						var.window.set_color(2)
						var.window.write('main','F',(x-var.camera[0],y-var.camera[1]))
						var.window.set_color(1)
				else:
					if (x,y) == tuple(var.player.loc):
						var.window.write('main','@',(x-var.camera[0],y-var.camera[1]))
					else:
						var.window.write('main',' ',(x-var.camera[0],y-var.camera[1]))
		
		var.window.refresh('main')