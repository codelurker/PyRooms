#!/usr/bin/python2
import functions, people, var, ai, rooms, towns, dungeons, words,  biomes, families, random
import items as item
import jobs as job

random.seed()

class controller:
	def __init__(self):
		self.map = []
		self.date = [1,0]
		self.ticks = 1
		self.history = []
		self.errors = []
		self.time = [0,0,1]
		
		self.id = 0
		self.people = []
		self.monsters = []
		self.jobs = []
		
		#Biomes
		self.forests = []
		self.rivers = []
		self.lakes = []
	
	def log(self,text,error=False):
		#if len(self.history) and text == self.history[len(self.history)-1] and not self.history[len(self.history)-1].count('Again.'):
		#	self.history[len(self.history)-1] += ' Again.'
		#elif len(self.history) and self.history[len(self.history)-1].count('Again.'):
		#	pass		
		#else:
		if len(self.history)==15: self.history.pop(0)
		self.history.append(text)
		
		if not error:
			var.window.clear('log')
			for i in range(len(self.history)):
				var.window.write('log',self.history[i],(0,i))
				var.window.refresh('log')
				var.window.refresh('main')
				i+=1
		else:
			self.errors.append(text)
		
	def status(self,text):
		var.window.write('status',text,(0,1))
		var.window.refresh('status')
		
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
					.size[1]/2)),avoidType='lake')
			path.extend(p.getPath())
		
		for pos in path:
			if self.map[pos[0]][pos[1]] == None:
				self.build_road(pos)
	
	def make_biome(self,list,type,num=4):
		for _f in range(num):
			pos = None
			
			while not pos:
				if type == 'forest':
					_dir = None
					_pos = (random.randint(1,var.world_size[0]-2),random.randint(1,var.world_size[1]-2))
				
				elif type == 'lake':
					_dir = None
					_pos = (random.randint(1,var.world_size[0]-2),random.randint(1,var.world_size[1]-2))
				
				elif type == 'river':
					_dir = random.randint(1,2) 
					
					if _dir == 1:
						_pos = (random.randint(1,var.world_size[0]-2),1)
						_dir = 'south'
					elif _dir == 2:
						_pos = (1,random.randint(1,var.world_size[1]-2))
						_dir = 'east'
				
				count = 0
				for f in self.forests:
					if (abs(_pos[0]-f.loc[0])+abs(_pos[1]-f.loc[1]))<=var.biome_distance:
						count+=1
				
				if not count:
					pos = _pos
				else:
					print 'Retrying'
			
			r = biomes.biome(pos,type,dir=_dir)
			list.append(r)
		
		for b in list:
			b.generate()
	
	def make_dungeon(self,num=1):
		for _f in range(num):
			d = dungeons.dungeon((2,2))
			#d.generate()
			#d.iterate()
			self.map[1][1].generate()
			self.map[1][1].dungeons.append(d)
			self.map[1][1].map[2][2]='stairsdown'
	
	def generate(self):
		#Make a blank map
		for x in range(var.world_size[0]):
			if var.debug: print '.',
			ycols = []
			
			for y in range(var.world_size[1]):
				ycols.append(None)
			
			self.map.append(ycols)

		#Make rivers and lakes
		#self.make_biome(self.rivers,'river',num=2)
		self.make_biome(self.lakes,'lake',num=4)
		
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
					spots.append((tspot[0]+x,tspot[1]+y))
			
			_t = towns.town(tspot,spots,self)
			_t.generate()
			self.towns.append(_t)
		
		#Connect towns
		#self.path_maker(self.towns)

		#Forests
		self.make_biome(self.forests,'forest',num=5)
		
		#Make field
		for x in range(var.world_size[0]):
			for y in range(var.world_size[1]):
				if not self.map[x][y]:
					self.build_field((x,y))

		#Dungeons
		self.make_dungeon()
		
		#Finish up by finding room exits
		l = None
		for x in range(1,var.world_size[0]-1):
			for y in range(1,var.world_size[1]-1):
				if self.map[x][y]:
					self.map[x][y].find_exits()
					l = self.map[x][y]
		
		#Make families
		for town in self.towns:
			for house in town.houses:
				families.family('Kraft',house).generate()
	
	def build_clearing(self,pos):
		r = rooms.room(pos,self)
		r.type = 'clearing'
		r.flags['sunlit'] = True
		r.randomize()
		
		self.map[pos[0]][pos[1]] = r
	
	def build_field(self,pos):
		r = rooms.room(pos,self)
		r.type = 'field'
		r.flags['sunlit'] = True
		r.randomize()
		
		self.map[pos[0]][pos[1]] = r
	
	def build_road(self,pos):
		r = rooms.room(pos,self)
		r.type = 'road'
		r.flags['sunlit'] = True
		
		self.map[pos[0]][pos[1]] = r
	
	def build_house(self,pos):
		r = rooms.room(pos,self)
		r.type = 'house'
		r.generate()
		r.randomize()

		self.map[pos[0]][pos[1]] = r
		
	def add_job(self,job):
		self.jobs.append(job)
	
	def make_human_race(self):
		var.player = people.human(player=True)
		var.player.name = ['Player','Derp']
		var.player.male = False
		var.player.age = 25
		var.player.strength = 4
		var.player.dexterity = 5
		var.player.intelligence = 3
		var.player.charisma = 8
		
		#var.player.warp_to(list(self.get_random_town().loc))
		var.player.warp_to([1,1])
		var.player.birthplace = var.player
		var.player.add_item(item.get_item('light'))
		
		var.camera[0] = var.player.loc[0]-40
		var.camera[1] = var.player.loc[1]-12
		if var.camera[0]<0: var.camera[0] = 0
		if var.camera[1]<0: var.camera[1] = 0
	
	def is_daytime(self):
		return True
	
	def tick(self,ticks=1):
		if var.debug: print 'Ticking',
		
		for _t in range(1,ticks+1):
			if var.debug: print '.',
			
			if var.player.in_room:
				var.player.get_room().noises = []
			
			var.player.player_tick()
			
			for _p in self.people:
				_p.tick()
			
			for _m in self.monsters:
				_m.tick()
			
			self.ticks += 1
			
			if not self.time[2] >= 59:
				self.time[2] += 1
			else:
				if self.time[1] < 60:
					self.time[1] += 1
				else:
					self.time[0] += 1
					self.time[1] = 0
				
				self.time[2] = 0
			
			
			if self.ticks == 14400:
				self.date[0]=1
				self.date[1]+=1
				self.ticks = 0
				
				if var.debug: print '[Time] It is now year %s.' % self.date[1]
				
				for _p in self.people:
					_p.events['lastbirthday']=False
		
		if not var.player.in_room:
			var.camera[0] = var.player.loc[0]-(var.win_size[0]/2)
			var.camera[1] = var.player.loc[1]-(var.win_size[1]/2)
		elif var.player.in_dungeon:
			var.camera[0] = var.player.room_loc[0]-(13)
			var.camera[1] = var.player.room_loc[1]-(var.win_size[1]/2)
		
		if var.camera[0]<0: var.camera[0] = 0
		if var.camera[1]<0: var.camera[1] = 0
		
		if var.player.in_room and not var.player.in_dungeon:
			var.player.get_room().tick()
		
		if var.player.in_dungeon:
			var.player.get_room().dungeons[0].tick()
		
		self.draw_map()
		if var.debug: print 'Done!\n',
	
	def tick_year(self,amnt):
		if amnt == 1:
			pass
			#self.log('[Time] Advancing 1 year.')
		else:
			self.log('[Time] Advancing %s years.' % amnt)
		
		for _y in range(14400*amnt):
			var.player.player_tick()
			
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
	
	def draw_tile(self,x,y,tile,color=True):
		if tile == 'clear':
			var.window.write('main',' ',(x,y))
		elif tile == 'grass':
			if color: var.window.set_color(3)
			var.window.write('main','.',(x,y))
			if color: var.window.set_color(1)
		elif tile == 'tree':
			if color: var.window.set_color(2)
			var.window.write('main','F',(x,y))
			if color: var.window.set_color(1)
		elif tile == 'wall':
			if color: var.window.set_color(6)
			var.window.write('main','#',(x,y))
			if color: var.window.set_color(1)
		elif tile == 'floor':
			if color: var.window.set_color(8)
			var.window.write('main','.',(x,y))
			if color: var.window.set_color(1)
		elif tile == 'stairsdown':
			if color: var.window.set_color(6)
			var.window.write('main','>',(x,y))
			if color: var.window.set_color(1)
	
	def draw_map(self):
		if not var.player.in_room:
			for _y in range(var.camera[1],var.camera[1]+var.win_size[1]-1):
				for _x in range(var.camera[0],var.camera[0]+var.win_size[0]):
					x = int(_x)
					y = int(_y)
					
					if x>=var.world_size[0]-1:
						x = var.world_size[0]-1
					
					if y>=var.world_size[1]-1:
						y = var.world_size[1]-1
					
					if self.map[x][y]:
						if self.map[x][y].type == 'house':
							var.window.write('main','H',(x-var.camera[0],y-var.camera[1]))
						elif self.map[x][y].type == 'clearing':
							var.window.set_color(5)
							var.window.write('main','.',(x-var.camera[0],y-var.camera[1]))
							var.window.set_color(1)
						if self.map[x][y].type == 'field':
							var.window.write('main',' ',(x-var.camera[0],y-var.camera[1]))						
						elif self.map[x][y].type == 'lake':
							var.window.set_color(4)
							var.window.write('main','.',(x-var.camera[0],y-var.camera[1]))
							var.window.set_color(1)					
						elif self.map[x][y].type == 'river':
							var.window.set_color(4)
							var.window.write('main','.',(x-var.camera[0],y-var.camera[1]))
							var.window.set_color(1)
						elif self.map[x][y].type == 'road':
							var.window.write('main','.',(x-var.camera[0],y-var.camera[1]))
						elif self.map[x][y].type == 'forest':
							var.window.set_color(2)
							var.window.write('main','F',(x-var.camera[0],y-var.camera[1]))
							var.window.set_color(1)
					
					for p in var._c.people:
						if (x,y) == tuple(p.loc):
							var.window.write('main','@',(x-var.camera[0],y-var.camera[1]))
					
					if (x,y) == tuple(var.player.loc):
						var.window.write('main','@',(x-var.camera[0],y-var.camera[1]))
		
		elif var.player.in_room and not var.player.in_dungeon:
			room = var.player.get_room()
			
			for y in range(0,var.room_size[1]):
				for x in range(0,var.room_size[0]):
					self.draw_tile(x+var.offset[0],y+var.offset[1],room.map[x][y])
					
					for item in room.objects:
						if (x,y) == tuple(item.room_loc):
							var.window.write('main',item.icon,(x+var.offset[0],y+var.offset[1]))
					
					for guest in room.guests:
						if (x,y) == tuple(guest.room_loc):
							var.window.write('main',guest.icon,(x+var.offset[0],y+var.offset[1]))
					
					if not room.lmap[x][y]: var.window.write('main',' ',(x+var.offset[0],y+var.offset[1]))
		
		elif var.player.in_dungeon:
			room = var.player.get_room().dungeons[0]
			
			for _y in range(var.camera[1],var.camera[1]+var.win_size[1]):
				for _x in range(var.camera[0],var.camera[0]+(26)):
					x = int(_x)
					y = int(_y)
					
					if x>=var.dungeon_size[0]-1:
						x = var.dungeon_size[0]-1
					
					if y>=var.dungeon_size[1]-1:
						y = var.dungeon_size[1]-1
					
					if not room.lmap[x][y]:
						if room.fmap[x][y]:
							self.draw_tile(x-var.camera[0],y-var.camera[1],room.map[x][y],color=False)
						else:
							var.window.write('main',' ',(x-var.camera[0],y-var.camera[1]))
					else:
						self.draw_tile(x-var.camera[0],y-var.camera[1],room.map[x][y])
					
					for guest in room.guests:
						if (x,y) == tuple(guest.room_loc):
							var.window.write('main','@',(x-var.camera[0],y-var.camera[1]))
		
		var.window.refresh('main')