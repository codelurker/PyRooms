import random, var

class dungeon:
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
	
	def draw_map(self):
		for x in range(0,self.size[0]):
			for y in range(0,self.size[1]):
				if self.fin_map[x][y]=='wall':
					print '#',
				else:
					print ' ',
			
			print

#m = dungeon((0,0))
#m.generate()
#m.iterate()
#m.draw_map()