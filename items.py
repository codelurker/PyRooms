#!/usr/bin/python2
import functions, words, var, os, copy

class item:
	def __init__(self):
		var.items.append(self)
		
		self.type = None
		self.owner = None
		self.room = None
		
		self.prefix = ''
		self.name = ''
		self.action = ''
		self.place = ''
		self.loc = [0,0]
		self.room_loc = [0,1]
		self.location = ''
		
		self.in_use = False
		self.user = None
		self.blocking = False
		
		self.wearable = False
		self.container = False
		self.stackable = False
		self.groupable = False
		self.surface = False
		self.chair = False
		
		self.smashable = False
		self.weight = 0
		self.contains = []
		self.max_contain = 5
		self.max_stack = 2
		self.active = False #True = Someone is sitting on it, light is on, etc
		
		self.stat = {'price':0,'damage':0,'defense':0}
		
	def sanitize(self,text,tag):
		return text.rpartition(tag)[0].split('|')[0]+' '+words.get_desc_light_filler(self)+'.'
	
	def attacked(self,by,wep):
		if self.smashable and self.blocking:
			self.blocking = False
	
	def sit_on(self,object):
		self.location = object.location+' on a %s' % object.name
		self.place = object.place
		self.parent = object
		object.contains.append(self)
	
	def take(self,who):
		if self in self.get_room().objects:
			self.get_room().objects.remove(self)

		self.owner = who

		self.parent = None
		who.items.append(self)
	
	def get_room(self):
		return var._c.map[self.loc[0]][self.loc[1]]
	
	def get_visual_description(self):
		return self.parse_description()
	
	def get_room_description(self):
		return self.room_description.replace('%prefix%',self.prefix[0].upper()+self.prefix[1:])\
		.replace('%ref%',self.name).replace('%action%',self.action)\
		.replace('%pos%',self.location)\
		.replace('%place%',self.place)\
		.replace('%roomtype%',self.get_room().type)
	
	def parse_description(self):
		return words.cut_text(self.description,self.get_room().get_lights())

	def destroy(self):
		self.get_room().objects.remove(self)

class container(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'container'
		self.container = True
	
	def put(self,item,where):
		self.contains.append({'item':item,'where':where})

class table(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'table'
		self.contains = []
	
	def get_description(self):
		return self.parse_description()

class light(item):
	def __init__(self):
		item.__init__(self)

		self.type = 'light'
		self.parent = None

		self.lit = True

	def get_description(self):
		if self.lit:
			if self.parent:
				return self.description.replace('%parent%',self.parent.name).replace('|','')
			else:
				return self.sanitize(self.description,'%parent%')

class foliage(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'foliage'
	
	def get_description(self):
		return self.parse_description()

class clothing(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'clothing'
		self.wearable = True
	
	def get_description(self):
		return self.parse_description()

class window(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'window'
		self.blocking = True
		self.smashable = True
	
	def attacked(self,by,wep):
		item.attacked(self,by,wep)
		
		if wep in ['lhand','rhand']:
			by.condition[wep]-=1
			by.bleeding[wep] = 5
			self.destroy()
			
			var._c.log('The glass breaks. Tiny shards cut into your %s.' % (words.translate[wep]))
	
	def get_description(self):
		return self.parse_description()

class weapon(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'weapon'
		self.wielding = False
	
	def get_description(self):
		return self.parse_description()
		
class corpse(item):
	def __init__(self,name,loc,room_loc):
		item.__init__(self)
		
		self.name = 'corpse of %s' % name[0]
		self.type = 'corpse'
		self.loc = loc
		self.room_loc = room_loc
		self.icon = '@'
		
		self.weight = 500
	
	def get_description(self):
		return self.parse_description()

def get_item(type):
	_l = []
	
	for item in var.items:
		if item.type == type:
			_l.append(copy.copy(item))
	
	if _l:
		return _l[functions.random.randint(0,len(_l)-1)]
	else:
		print 'Couldn\'t get any items of type %s' % type

def get_item_name(name):
	_l = []
	
	for item in var.items:
		if item.name == name:
			_l.append(copy.copy(item))
	
	if _l:
		return _l[functions.random.randint(0,len(_l)-1)]
	else:
		print 'Couldn\'t get any items of type %s' % type

def get_item_clothing(slot):
	_l = []
	
	for item in var.items:
		if item.type == 'clothing' and item.slot == slot:
			_l.append(copy.copy(item))
	
	if _l:
		return _l[functions.random.randint(0,len(_l)-1)]
	else:
		print 'Couldn\'t get any items of type %s' % type