import var, people, words, random
import items as item

class family:
	def __init__(self, name, loc):
		self.name = name
		self.loc = loc
		
		self.tree = []
	
	def generate(self):
		#Find the house they'll be generated in.
		_r = var._c.map[self.loc[0]][self.loc[1]]
		_r.tick(light=False)
		
		self.house = None
		while not self.house:
			for space in _r.walkingspace:
				if random.randint(0,15) <= 1:
					self.house = (space[0],space[1])
					break
		
		#Generate a husband and wife
		husband = people.human()
		husband.name = [words.get_name(husband.race,husband.male),self.name]
		husband.age = 30
		husband.strength = 6
		husband.dexterity = 4
		husband.intelligence = 6
		husband.charisma = 6
		husband.add_item(item.get_item_clothing('chest'))
		husband.add_item(item.get_item_clothing('feet'))
		husband.add_item(item.get_item_clothing('head'))
		husband.add_item(item.get_item_clothing('torso'))
		husband.wear(husband.items[0])
		husband.wear(husband.items[1])
		husband.wear(husband.items[2])
		husband.wear(husband.items[3])
		husband.warp_to(list(self.loc))
		husband.room_loc = list(self.house)
		husband.enter_room()
		
		self.house = None
		while not self.house:
			for space in _r.walkingspace:
				if random.randint(0,15) <= 1:
					self.house = (space[0],space[1])
					break
		
		wife = people.human()
		wife.male = False
		wife.name = [words.get_name(wife.race,wife.male),self.name]
		wife.age = 30
		wife.strength = 6
		wife.dexterity = 4
		wife.intelligence = 6
		wife.charisma = 6
		wife.add_item(item.get_item_clothing('chest'))
		wife.add_item(item.get_item_clothing('feet'))
		wife.add_item(item.get_item_clothing('head'))
		wife.add_item(item.get_item_clothing('torso'))
		wife.wear(wife.items[0])
		wife.wear(wife.items[1])
		wife.wear(wife.items[2])
		wife.wear(wife.items[3])
		wife.warp_to(list(self.loc))
		wife.room_loc = list(self.house)
		wife.enter_room()
		
		dog = people.dog()
		dog.tamed = True
		dog.owner = husband
		dog.name = 'Albert'
		dog.warp_to(list(self.loc))
		dog.room_loc = [2,1]
		dog.enter_room()