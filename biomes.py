import ai, var, controller

class biome:
	def __init__(self, loc, type, dir=None):
		self.type = type
		self.loc = loc
		self.walk_dir = dir
		
		if self.type == 'forest':
			self.green = 40
		elif self.type == 'river':
			self.green = 30
		elif self.type == 'lake':
			self.green = 30
	
	def generate(self):
		for pos in [[0,-1],[-1,0],[1,0],[0,1]]:
			r = controller.room((self.loc[0]+pos[0],self.loc[1]+pos[1]),var._c)
			r.parent_pos = self.loc
			r.type = self.type
			r.flags['sunlit'] = True
			r.green = self.green - 10
			r.walk_dir = self.walk_dir
			r.randomize()
			var._c.map[self.loc[0]+pos[0]][self.loc[1]+pos[1]] = r