import random, ai, words, var
import items as item

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
		self.dungeons = []
		
		self.map = []
		self.lmap = []
		self.exits = []
		self.noises = []
		
		self.flags = {'sunlit':False}
		
	def generate(self):
		for y in range(0,var.room_size[1]+1):
			self.lmap.append([0] * var.room_size[0])
			if self.type == 'house': self.map.append(['clear'] * (var.room_size[0]))
		
		if self.type == 'house':
			self.house = {'spos':(random.randint(0,(var.room_size[0]/2)-4),random.randint(1,(var.room_size[1]/2)-4)),\
							'size':random.randint(4,10),'windows':random.randint(1,6)}
			windows = 0
			self.walls = []
			self.walkingspace = []
			
			for n in range(6):
				size = (15,15)
				pos = (random.randint(3,size[0]-5),random.randint(4,size[1]-5))
				_size = (random.randint(3,size[0]-pos[0]),random.randint(3,size[1]-pos[1]))
				
				for x in range(_size[0]):
					for y in range(_size[1]):
						if x == 0 or x == (_size[0])-1 or y == 0 or y == (_size[1])-1:
							if self.map[pos[0]+x][pos[1]+y] == 'clear':
								self.map[pos[0]+x][pos[1]+y] = 'wall'
								self.walls.append([pos[0]+x,pos[1]+y])	
						else:
							self.map[pos[0]+x][pos[1]+y] = 'floor'
							self.walkingspace.append([pos[0]+x,pos[1]+y])
			
			#Remove walking space from self.walls array
			for place in self.walkingspace:
				if place in self.walls: self.walls.remove(place)
	
			#Grass
			for x in range(0,var.room_size[0]):
				for y in range(0,var.room_size[1]):
					if not [x,y] in self.walls and not [x,y] in self.walkingspace and random.randint(1,6) <= 1:
						self.map[x][y] = 'grass'						
		
		for x in range(0,var.room_size[0]):
			ycols = []
			
			if self.type == 'house':
				break
			
			for y in range(0,var.room_size[1]):				
				if self.type == 'clearing':
					if random.randint(0,8) == 1:
						type = 'grass'
					else:
						type = 'clear'
				
				elif self.type == 'lake':
					type = 'clear'
				
				#elif self.type == 'house':
				
				
				elif self.type == 'field':
					if random.randint(0,4) <= 2:
						type = 'grass'
					else:
						type = 'clear'
				
				elif self.type == 'forest':
					green = self.get_green()
					
					if green == 0:
						g = 30
					elif green == 1:
						g = 25
					elif green == 2:
						g = 15
					elif green >= 3:
						g = 10
					
					num = random.randint(0,g)
					if num <= 2:
						type = 'grass'
					elif num == 3:
						type = 'tree'
					else:
						type = 'clear'

				ycols.append(type)
			

			self.map.append(ycols)
			
			#for self.
	
	def randomize(self):
		if self.type == 'clearing':
			for n in range(0,random.randint(0,1)):
				_i = item.get_item('foliage')
				_i.loc = self.loc
				self.add_object(_i)
		
		elif self.type == 'house':
			_d = item.get_item_name('iron dagger')
			_d.room_loc = [2,2]
			self.add_object(_d)
			
			#Decorate~~!!
			
			#Windows - Corner check.
			for wall in self.walls:
				if random.randint(1,8) <= 1:
					_h = 0
					_v = 0
					for pos in [[-1,0],[1,0]]:
						if [wall[0]+pos[0],wall[1]+pos[1]] in self.walls:
							_h += 1
					
					for pos in [[0,-1],[0,1]]:
						if [wall[0]+pos[0],wall[1]+pos[1]] in self.walls:
							_v += 1
					
					if _h == 2 and not _v or _v == 2 and not _h:
						self.map[wall[0]][wall[1]] = 'grass'
						_i = item.get_item('window')
						_i.room_loc = [wall[0],wall[1]]
						self.add_object(_i)	
			
			#_t = item.get_item_name('table')
			#_t.room_loc=[pos[0],pos[1]]
			#self.add_object(_t)
			
		elif self.type == 'forest':
			_ws = []
			for w in range(self.green/10):
				_w = ai.RandomWalker(self.loc)
				_w.walk()
				_ws.append(_w)
			
			for w in _ws:
				for _pos in w.path:
					if _pos[0]>0 and _pos[0]<var.world_size[0]-2 and _pos[1]>0 and _pos[1]<var.world_size[1]-2 and not var._c.map[_pos[0]][_pos[1]]:
						r = room(_pos,var._c)
						r.type = 'forest'
						r.flags['sunlit'] = True
						r.green = self.green - 10
						r.randomize()
						
						var._c.map[_pos[0]][_pos[1]] = r
		
		elif self.type == 'lake':
			_ws = []
			for w in range(self.green/10):
				_w = ai.RandomWalker(self.loc,bold=True)
				_w.walk()
				_ws.append(_w)
			
			for w in _ws:
				for _pos in w.path:
					if _pos[0]>0 and _pos[0]<var.world_size[0]-2 and _pos[1]>0 and _pos[1]<var.world_size[1]-2 and not var._c.map[_pos[0]][_pos[1]]:
						r = room(_pos,var._c)
						r.type = 'lake'
						r.flags['sunlit'] = True
						r.green = self.green - 10
						r.randomize()
						
						var._c.map[_pos[0]][_pos[1]] = r
		
		elif self.type == 'river':
			_ws = []
			for w in range(self.green/10):
				if self.walk_dir == 'south':
					_xchange = 5
					_ychange = 0
				elif self.walk_dir == 'east':
					_xchange = 0
					_ychange = 15
				
				_w = ai.DirectionalWalker(self.loc,self.walk_dir,xchange=_xchange,ychange=_ychange)
				_w.walk()
				_ws.append(_w)
			
			for w in _ws:
				for _pos in w.path:
					if _pos[0]>0 and _pos[0]<var.world_size[0]-2 and _pos[1]>0 and _pos[1]<var.world_size[1]-2 and (not var._c.map[_pos[0]][_pos[1]] or var._c.map[_pos[0]][_pos[1]].type == 'forest'):
						r = room(_pos,var._c)
						r.type = 'river'
						r.flags['sunlit'] = True
						r.green = self.green - 10
						r.walk_dir = self.walk_dir
						r.randomize()
						
						var._c.map[_pos[0]][_pos[1]] = r
				
	def tick(self):
		lights = []
		
		self.lmap = []
		for x in range(0,var.room_size[0]):
			ycols = []
			for y in range(0,var.room_size[1]):	
				if not self.type == 'house' and self.flags['sunlit']:
					ycols.append(1)
				else:
					ycols.append(0)
			
			self.lmap.append(ycols)
		
		if not self.type == 'house' and self.flags['sunlit']: return True
		
		lights = []
		for obj in self.objects:
			if obj.type in ['light']:
				lights.append(obj)
		
		for guest in self.guests:
			for obj in guest.items:
				if obj.type == 'light':
					lights.append(obj)
		
		for obj in lights:
			for y in range(-24,25):
				for x in range(-24,25):
					if not 0 < obj.room_loc[0]+x < var.room_size[0] and not 0 < obj.room_loc[1]+y < var.room_size[1]: continue
					if (abs(obj.room_loc[0]-(obj.room_loc[0]+x))+abs(obj.room_loc[1]-(obj.room_loc[1]+y))) > 15: continue
					
					if (obj.room_loc[0],obj.room_loc[1]) == (obj.room_loc[0]+x,obj.room_loc[1]+y): continue
					
					l = ai.line((obj.room_loc[0],obj.room_loc[1]),(obj.room_loc[0]+x,obj.room_loc[1]+y))
						
					if not l.path[0] == (obj.room_loc[0],obj.room_loc[1]):
						l.path.reverse()
												
					done = False
					for lpos in l.path:
						if done: break				
						
						if lpos[0]>=0 and lpos[0]<var.room_size[0] and lpos[1]>=0 and lpos[1]<var.room_size[1]:
							if not self.map[lpos[0]][lpos[1]]=='wall':
								self.lmap[lpos[0]][lpos[1]] = 1
							else:
								self.lmap[lpos[0]][lpos[1]] = 1
								done = True
	
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
	
	def get_green(self):
		g = 0
		for pos in [[0,-1],[-1,0],[1,0],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]]:
			if self.controller.map[self.loc[0]+pos[0]][self.loc[1]+pos[1]].type == 'forest':
				g += 1
		
		return g
	
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
		
		#if self.type == 'house':
		#	for exit in self.exits:
		#		_i = item.get_item('window')
		#		_i.place = exit['dir']
		#		_i.inside = self
		#		_i.outside = exit['room']
		#		
		#		if _i.place == 'west':
		#			_i.room_loc = [1,12]
		#		elif _i.place == 'east':
		#			_i.room_loc = [23,12]
		#		elif _i.place == 'north':
		#			_i.room_loc = [12,2]
		#		elif _i.place == 'south':
		#			_i.room_loc = [12,22]
		#		
		#		exit['obj'] = _i
		#		self.add_object(_i)
				
	def add_object(self,obj,place=None):
		obj.loc = self.loc
		if not place:
			obj.location = words.get_phrase('location')
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