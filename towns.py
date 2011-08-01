class town:
	def __init__(self, loc, map, controller):
		self.name = 'DeathTown 2K11'
		self.loc = loc
		self.map = map
		self.size = map[len(map)-1][1]-map[0][1]+1
		
		self.controller = controller
		
	def get_population(self):
		for pos in self.map:
			for guest in self.controller.map[pos[0]][pos[1]].guests:
				print guest
	
	def generate(self):
		#Clear out map
		for pos in self.map:
			self.controller.build_clearing(pos)
		
		#Start placing housing based on size
		