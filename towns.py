class town:
	def __init__(self, loc, map, controller):
		self.name = 'DeathTown 2K11'
		self.loc = loc
		self.map = map
		self.controller = controller
		
	def generate(self):
		for pos in self.map:
			self.controller.build_clearing(pos)