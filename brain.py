class brain:
	def __init__(self,owner):
		self.owner = owner
		
		self.locations = [] #name:name, coords:x,y, map:[{start:startpos,map:map}]
		