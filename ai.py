import var

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
				else:
					if not self.astar.map[npos[0]][npos[1]] == None and not self.astar.map[npos[0]][npos[1]] in self.astar._cl:
						_n.append(self.astar.map[npos[0]][npos[1]])
		
		return _n

class AStar:
	def __init__(self,start,end,debug=False,ignoreNone=False):
		self.map = []
		self.start = start
		self.end = end
		self._ol = []
		self._cl = []
		self.lowest = None
		self.chance = 0
		self.max_chances = 50
		self.ignoreNone = ignoreNone
		
		self.map = []
		for x in range(0,var.world_size[0]):
			_y = []
			for y in range(0,var.world_size[1]):
				if var._c.map[x][y] or ignoreNone:
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
			print 'Failed.'
		
		#Add starting point to open list
		self._ol.append(startnode)
		
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