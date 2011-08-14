import var, people
import items as item

class family:
	def __init__(self, name, loc):
		self.name = name
		self.loc = loc
		
		self.tree = []
	
	def generate(self):
		#Find the house they'll be generated in.
		_r = var._c.map[self.loc[0]][self.loc[1]]
		_r.tick()
		
		self.house = (_r.house['spos'][0]+1,_r.house['spos'][1]+1)
		
		#Generate a husband and wife
		husband = people.human()
		husband.name = ['Adam',self.name]
		husband.age = 30
		husband.strength = 6
		husband.dexterity = 4
		husband.intelligence = 6
		husband.charisma = 6
		husband.add_item(item.get_item_clothing('chest'))
		husband.add_item(item.get_item_clothing('feet'))
		husband.add_item(item.get_item_clothing('head'))		
		husband.wear(husband.items[0])
		husband.wear(husband.items[1])
		husband.wear(husband.items[2])
		husband.warp_to(list(self.loc))
		husband.room_loc = list(self.house)
		husband.enter_room()
		
		wife = people.human()
		wife.name = ['Eve',self.name]
		wife.age = 30
		wife.strength = 6
		wife.dexterity = 4
		wife.intelligence = 6
		wife.charisma = 6
		wife.add_item(item.get_item_clothing('chest'))
		wife.add_item(item.get_item_clothing('feet'))
		wife.add_item(item.get_item_clothing('head'))		
		wife.wear(wife.items[0])
		wife.wear(wife.items[1])
		wife.wear(wife.items[2])
		wife.warp_to(list(self.loc))
		wife.room_loc = list(self.house)
		wife.enter_room()