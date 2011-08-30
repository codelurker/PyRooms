import random, var, time, ai
import rooms

class cavern:
	def __init__(self, loc):
		self.loc = loc
		
		self.guests = []
		
		self.size = (var.dungeon_size[0],var.dungeon_size[1])
		self.map = []
		self.fin_map = []
		self.area = self.size[0]*self.size[1]
		self.border = 2
		self.open = .45
	
	def generate(self):
		for x in range(0,self.size[0]):
			y_col = []
			
			for y in range(0,self.size[1]):
					y_col.append('wall')
			
			self.map.append(y_col)
			self.fin_map.append(y_col)
		
		oc = (self.area * self.open)
		
		while oc > 0:
			pos = (random.randint(self.border,self.size[0]-self.border),random.randint(self.border,self.size[1]-self.border))
			
			if self.map[pos[0]][pos[1]]=='wall':
				self.map[pos[0]][pos[1]] = 'floor'
				oc -= 1
	
	def iterate(self):
		for z in range(1):
			for x in range(self.border,self.size[0]-self.border):
				for y in range(self.border,self.size[1]-self.border):
					wall = False
					count = 0
					
					if self.map[x][y]=='wall':
						wall = True
					
					for pos in [[0,-1],[0,1],[-1,0],[1,0],[-1,-1],[1,-1],[-1,1],[1,1]]:
						npos = [x+pos[0],y+pos[1]]
						
						if self.map[npos[0]][npos[1]] == 'wall':
							count+=1
					
					if not wall:
						if count>5:
							self.fin_map[x][y] = 'wall'
					elif count<4:
						self.fin_map[x][y] = 'floor'

			self.map = self.fin_map
		
		for x in range(self.border,self.size[0]-self.border):
			for y in range(self.border,self.size[1]-self.border):
				for pos in [[0,-1],[0,1],[-1,0],[1,0],[-1,-1],[1,-1],[-1,1],[1,1]]:
					npos = [x+pos[0],y+pos[1]]
					
					if self.map[npos[0]][npos[1]] == 'wall':
						count+=1
				
				if count <= 0:
					self.fin_map[x][y] = 'wall'

class room:
	def __init__(self, spos, epos, map):
		self.spos = spos
		self.epos = epos
		self.map = map
		
		self.room = []
		self.walkingspace = []
		self.walls = []
		self.openwalls = []
		self.exits = []
		self.doors = []
		self.connected = False
		self.connected_to = [self]
		
		for x in range(self.epos[0]-self.spos[0]):
			self.room.append([None] * (self.epos[1]-self.spos[1]))
		
		self.generate()
		self.draw(self.map)
	
	def generate(self):
		for x in range(self.epos[0]-self.spos[0]):
			for y in range(self.epos[1]-self.spos[1]):
				if not self.room[x][y]:
					if y == 0 or x == 0 or self.spos[0]+x == self.epos[0]-1 or self.spos[1]+y == self.epos[1]-1:
						self.walls.append([x,y])
						self.room[x][y] = 'wall'
					else:
						self.room[x][y] = 'floor'
		
		#Find open walls (for doors/exits)
		for wall in self.walls:
			_h = 0
			_v = 0
			
			for horz in [[-1,0],[1,0]]:
				if [wall[0]+horz[0],wall[1]] in self.walls:
					_h += 1
			for vert in [[0,-1],[0,1]]:
				if [wall[0],wall[1]+vert[1]] in self.walls:
					_v += 1
			
			if _h and not _v:
				if wall[1] == 0:
					self.exits.append({'dir':'west','pos':wall})
				elif wall[1] == self.epos[1]-self.spos[1]-1:
					self.exits.append({'dir':'east','pos':wall})
			elif not _h and _v:
				if wall[0] == 0:
					self.exits.append({'dir':'north','pos':wall})
				elif wall[0] == self.epos[0]-self.spos[0]-1:
					self.exits.append({'dir':'south','pos':wall})
		
		for dir in random.sample(['north','south','east','west'],3):
			_placed = False
			
			while not _placed:
				for _exit in self.exits:
					if _exit['dir'] == dir:
						if random.randint(0,10)==1:
							self.room[_exit['pos'][0]][_exit['pos'][1]] = 'door'
							self.doors.append(_exit)
							_placed = True
							break
	
	def find_connections(self):
		for r in self.connected_to:
			for _r in r.connected_to:
				if _r == self: continue
				
				if not _r in self.connected_to: self.connected_to.append(_r)
		
		return self.connected_to
		
	def draw(self, _map):
		for x in range(self.epos[0]-self.spos[0]):
			for y in range(self.epos[1]-self.spos[1]):
				_map[self.spos[0]+x][self.spos[1]+y] = self.room[x][y]

class dungeon(rooms.room):
	def __init__(self,loc):
		rooms.room.__init__(self,loc,var._c,size=var.dungeon_size)
		
		self.rooms = []

	def generate(self):
		for x in range(0,var.dungeon_size[0]):
			self.map.append(['empty'] * var.dungeon_size[1])
			self.fmap.append([0] * self.size[0])
		
		for r in range(0,50):
			_pos = (random.randint(0,55),random.randint(0,55))
			
			_size = [0,5]
			if _pos[0] >= 20:
				_size[0] = 5
			else:
				_size[0] = random.randint(5,55-_pos[0])
			
			if _size[0] > 20: _size[0] = 10
			
			
			if _pos[1] >= 20:
				_size[1] = 5
			else:
				_size[1] = random.randint(5,55-_pos[1])
			
			if _size[1] > 20: _size[1] = 10
				
			_r = room(_pos,(_pos[0]+_size[0],_pos[1]+_size[1]),self.map)
			_r.center = (_pos[0]+(_size[0]/2),_pos[1]+(_size[1]/2))
			self.rooms.append(_r)

		#Clean rooms
		for y in range(0,var.dungeon_size[1]):
			for x in range(0,var.dungeon_size[0]):
				_c = 0
				
				if self.map[x][y] == 'wall':
					for pos in [[-1,0],[1,0],[0,-1],[0,1]]:
						if x < 60-1 and y < 60-1:
							if self.map[x+pos[0]][y+pos[1]] in ['floor','wall']:
								_c += 1
					
					if _c == 4:
						self.map[x][y] = 'floor'

		#Do first round of connections.
		#It's very rare that everything will be successful this time around.
		for _r in self.rooms:
			if len(_r.connected_to) == len(_r.doors): continue
			_r.closest = {'room':None,'dist':1000}
			
			for _r2 in self.rooms:
				if _r == _r2 or _r2 in _r.connected_to: continue
				_dist = abs(_r.center[0]-_r2.center[0])+abs(_r.center[1]-_r2.center[1])
				
				if _dist < _r.closest['dist']:
					_r.closest['room'] = _r2
					_r.closest['dist'] = _dist
				
			_r.connected_to.append(_r.closest['room'])
			_r.closest['room'].connected_to.append(_r)
			
			door = _r.doors[random.randint(0,len(_r.doors)-1)]
			door2 = _r.closest['room'].doors[random.randint(0,len(_r.closest['room'].doors)-1)]
			a = ai.AStar((_r.spos[0]+door['pos'][0],_r.spos[1]+door['pos'][1]),(_r.closest['room'].spos[0]+door2['pos'][0],_r.closest['room'].spos[1]+door2['pos'][1]),size=var.dungeon_size,omap = self.map,room=True)
			
			for pos in a.getPath():
				self.map[pos[0]][pos[1]] = 'floor'

		#Connect "broken" rooms
		#Broken == not connected to other rooms
		#We do this by taking each room and iterating through each room it's connected to
		#and adding each room that room is connected to. By the end, we compare that list
		#to the master list of rooms. If that list differs, we connect the rooms that are
		#missing.
		self.fix_rooms()
		
		for y in range(0,var.dungeon_size[1]):
			for x in range(0,var.dungeon_size[0]):
				if self.map[x][y] in ['empty','door']:
					self.map[x][y] = 'wall'
				if self.map[x][y] == 'floor':
					self.walkingspace.append([x,y])
	
	def fix_rooms(self):
		stime1 = time.time()
		_maps = []

		for _r in self.rooms:
			_ret = _r.find_connections()
			_temp = []
			
			for _room in _ret:
				if not _room in _temp:
					_temp.append(_room)
			
			_temp.sort()
			if not _temp in _maps:
				_maps.append(_temp)
			
		#print 'Connecting %s sections...' % (len(_maps))
		
		for i in range(len(_maps)):
			if not i: continue
			stime2 = time.time()
			if var.debug: var._c.log('Iter %s took' % (i))
			
			door = _maps[i-1][0].doors[random.randint(0,len(_maps[i-1][0].doors)-1)]
			door2 = _maps[i][0].doors[random.randint(0,len(_maps[i][0].doors)-1)]
			a = ai.AStar((_maps[i-1][0].spos[0]+door['pos'][0],_maps[i-1][0].spos[1]+door['pos'][1]),(_maps[i][0].spos[0]+door2['pos'][0],_maps[i][0].spos[1]+door2['pos'][1]),size=var.dungeon_size,omap = self.map,room=True)
			
			for pos in a.getPath():
				self.map[pos[0]][pos[1]] = 'floor'
			if var.debug: var._c.log(time.time()-stime2)
		
	def get_open_space(self):
		while 1:
			for walking in self.walkingspace:
				if random.randint(0,10) <= 1: return walking
	
	def tick(self):
		self.lmap = []
		for x in range(0,var.dungeon_size[0]):
			ycols = []
			for y in range(0,var.dungeon_size[1]):	
				ycols.append(0)
			
			self.lmap.append(ycols)
		
		for y in range(-var.player.perception-(10-var.player.condition['eyes']),var.player.perception-(10-var.player.condition['eyes'])):
			for x in range(-24,25):
				if not 0 < var.player.room_loc[0]+x < var.dungeon_size[0] and not 0 < var.player.room_loc[1]+y < var.dungeon_size[1]: continue
				if (abs(var.player.room_loc[0]-(var.player.room_loc[0]+x))+abs(var.player.room_loc[1]-(var.player.room_loc[1]+y))) > 15: continue
				
				if (var.player.room_loc[0],var.player.room_loc[1]) == (var.player.room_loc[0]+x,var.player.room_loc[1]+y): continue
				
				l = ai.line((var.player.room_loc[0],var.player.room_loc[1]),(var.player.room_loc[0]+x,var.player.room_loc[1]+y))
					
				if not l.path[0] == (var.player.room_loc[0],var.player.room_loc[1]):
					l.path.reverse()
											
				done = False
				for lpos in l.path:
					if done: break				
					
					if lpos[0]>=0 and lpos[0]<var.dungeon_size[0] and lpos[1]>=0 and lpos[1]<var.dungeon_size[1]:
						if not self.map[lpos[0]][lpos[1]]=='wall':
							self.lmap[lpos[0]][lpos[1]] = 1
							if not [lpos[0],lpos[1]] in self.fmap: self.fmap.append([lpos[0],lpos[1]])
						else:
							self.lmap[lpos[0]][lpos[1]] = 1
							if not [lpos[0],lpos[1]] in self.fmap: self.fmap.append([lpos[0],lpos[1]])
							done = True