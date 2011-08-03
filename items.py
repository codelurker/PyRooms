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
		self.loc = (0,0)
		self.location = ''
		
		self.wearable = False
		self.container = False
		self.stackable = False
		self.groupable = False
		self.surface = False
		self.chair = False
		
		self.weight = 0
		self.contains = []
		self.max_contain = 5
		self.max_stack = 2
		self.active = False #True = Someone is sitting on it, light is on, etc
		
	def sanitize(self,text,tag):
		return text.rpartition(tag)[0].split('|')[0]+' '+words.get_desc_light_filler(self)+'.'
	
	def sit_on(self,object):
		self.location = object.location+' on a %s' % object.name
		self.place = object.place
		self.parent = object
		object.contains.append(self)
	
	def take(self,who):
		self.get_room().objects.remove(self)
		self.place = ''
		self.location = 'in %s\'s inventory' % who.name
		
		if self.parent: self.parent.contains.remove(self)
		
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

		self.on = True

	def get_description(self):
		if self.on:
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
	
	def get_description(self):
		return self.parse_description()

def load_items():
	pass

def get_item(type):
	_l = []
	
	for item in var.items:
		if item.type == type:
			_l.append(copy.copy(item))
	
	if _l:
		return _l[functions.random.randint(0,len(_l)-1)]
	else:
		print 'Couldn\'t get any items of type %s' % type