import var, random

class Node:
	def __init__(self, loc, astar):
		self.loc = loc
		self.astar = astar
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0
	
	def getG(self):
		self.g = self.parent.g+10
	
	def getH(self,end):
		self.h = 10*(abs(self.loc[0]-end[0])+abs(self.loc[1]-end[1]))
	
	def getF(self):
		self.f = self.g+self.h
	
	def getAdj(self):
		_n = []
		
		for pos in [[0,-1],[-1,0],[1,0],[0,1]]:
			npos = [self.loc[0]+pos[0],self.loc[1]+pos[1]]
			
			if npos[0] >= 0 and npos[0] <= var.world_size[0] and npos[1] >= 0 and npos[1] <= var.world_size[1]:
				if self.astar.ignoreNone:
					if not self.astar.map[npos[0]][npos[1]] in self.astar._cl:
						_n.append(self.astar.map[npos[0]][npos[1]])
				
				elif self.astar.avoidType:
					if self.astar.map[npos[0]][npos[1]] and not self.astar.map[npos[0]][npos[1]] in self.astar._cl:
						_n.append(self.astar.map[npos[0]][npos[1]])
				
				else:
					if not self.astar.map[npos[0]][npos[1]] == None and not self.astar.map[npos[0]][npos[1]] in self.astar._cl:
						_n.append(self.astar.map[npos[0]][npos[1]])
		
		return _n

class AStar:
	def __init__(self,start,end,debug=False,ignoreNone=False,avoidType=False):
		self.map = []
		self.start = start
		self.end = end
		self._ol = []
		self._cl = []
		self.lowest = None
		self.chance = 0
		self.max_chances = var.astar_chances
		self.ignoreNone = ignoreNone
		self.avoidType = avoidType
		
		self.map = []
		for x in range(0,var.world_size[0]):
			_y = []
			for y in range(0,var.world_size[1]):
				if avoidType==False:
					if var._c.map[x][y] or ignoreNone:
						_y.append(Node((x,y),self))
					else:
						_y.append(None)
				else:
					if var._c.map[x][y] and not var._c.map[x][y].type == self.avoidType:
						_y.append(Node((x,y),self))
					else:
						_y.append(None)
				
			self.map.append(_y)
		
		if debug:
			import time
			_stime = time.time()
		
		if self.end:
			self.run(self.map[self.start[0]][self.start[1]])
		
		if debug: print time.time()-_stime
		
	def run(self, startnode):
		self.chance +=1
		if self.chance >= self.max_chances:
			var._c.log('Failed.')
		
		#Add starting point to open list
		self._ol.append(startnode)
		
		var._c.log(str(startnode.loc))
		
		#Get adjacent nodes
		_l = startnode.getAdj()
		
		for n in _l:
			#Not in open list, add it
			if not n in self._ol:
				n.parent = startnode
				n.getG()
				n.getH(self.end)
				n.getF()
				self._ol.append(n)
			else:
				if n.g < startnode.g:
					n.parent = startnode
					n.getG()
					n.getH(self.end)
					n.getF()
		
		#Drop starting square
		self._ol.remove(startnode)
		self._cl.append(startnode)
		
		#Check open list:
		for n in self._ol:
			if self.lowest == None or n.f <= self.lowest.f:
				if not n == self.lowest:
					self.lowest = n
		
		#Drop lowest
		if self.lowest.loc == self.end:
			return self.lowest
		else:
			if self.lowest in self._ol:
				if self.chance < self.max_chances:
					self._ol.remove(self.lowest)
					self._cl.append(self.lowest)
					self.run(self.lowest)
			else:
				for n in self._ol:
					if self.lowest == None or n.f <= self.lowest.f+20:
						self.lowest = n
				
				if self.chance < self.max_chances:
					self.run(self.lowest)

	def getPath(self):
		path = []
		node = self.lowest
		p = node
		
		while 1:
			if p:
				path.append(p.loc)
				node = p
			else:
				break
			
			p = node.parent
		
		path.pop()
		return path
	
	def drawPath(self,node):
		path = []
		p = node
		
		while 1:
			if p:
				path.append(p.loc)
				node = p
			else:
				break
			
			p = node.parent

		for y in range(0,var.world_size[0]):
			for x in range(0,var.world_size[1]):
				if (x,y) in path:
					print 'x',
				else:
					if self.map[x][y] == None:
						print '#',
					#elif self.map[x][y] in self._ol:
					#	print 'O',
					#elif self.map[x][y] in self._cl:
					#	print 'C',
					else:
						print '.',
			
			print

class Walker:
	def __init__(self,start,bold=0,width=0,xchange=0,ychange=0):
		self.pos = list(start)
		
		self.bold = bold
		self.width = width
		
		self.path = []
		self.life = 0
		
		self.xchange = xchange
		self.ychange = ychange
		self.lxchange = 0
		self.lychange = 0

	def walk(self):
		for w in range(self.max_life):
			dir = self.directions[random.randint(0,len(self.directions)-1)]
			
			if dir == 1:
				self.pos[0]-=1
				self.pos[1]+=1
			elif dir == 2:
				self.pos[1]+=1
			elif dir == 3:
				self.pos[0]+=1
				self.pos[1]+=1
			elif dir == 6:
				self.pos[0]+=1
			elif dir == 9:
				self.pos[0]+=1
				self.pos[1]-=1
			elif dir == 8:
				self.pos[1]-=1
			elif dir == 7:
				self.pos[0]-=1
				self.pos[1]+=1
			elif dir == 4:
				self.pos[0]-=1

			if len(self.path) and self.xchange:
				if self.lxchange >= self.xchange:
					self.lxchange = 0
				else:
					ldir = self.path[len(self.path)-1]
					self.pos[0] = ldir[0]
					self.lxchange += 1
			
			if len(self.path) and self.ychange:
				if self.lychange >= self.ychange:
					self.lychange = 0
				else:
					ldir = self.path[len(self.path)-1]
					self.pos[1] = ldir[1]
					self.lychange += 1
			
			self.path.append(list(self.pos))
			
			if self.bold:
				_l = list(self.pos)
				for pos in [[0,-1],[-1,0],[1,0],[0,1]]:
					self.path.append((_l[0]+pos[0],_l[1]+pos[1]))

class RandomWalker(Walker):
	def __init__(self,start,bold=0):
		Walker.__init__(self,start=start,bold=bold)
		
		self.directions = [[1,2,3],[2,3,6],[3,6,9],[6,9,8],[9,8,7],[8,7,4],[7,4,1],[4,1,2]]
		self.directions = self.directions[random.randint(0,len(self.directions)-1)]
		
		self.max_life = var.walker_life

class DirectionalWalker(Walker):
	def __init__(self,start,direction,bold=0,xchange=0,ychange=0):
		Walker.__init__(self,start=start,bold=bold,width=1,xchange=xchange,ychange=ychange)
		
		if direction == 'north':
			self.directions = [7,8,9]
		elif direction == 'south':
			self.directions = [1,2,3]
		elif direction == 'east':
			self.directions = [3,6,9]
		elif direction == 'west':
			self.directions = [1,4,7]
		
		self.max_life = var.walker_life*4

class BidirectionalWalker(Walker):
	def __init__(self,start):
		person.__init__(self,start=start)
		_direction1 = self.directions[random.randint(0,len(self.directions)-1)]
		_direction2 = [-n for n in _direction1]