#!/usr/bin/python2
import functions, words, var, os, copy
from BeautifulSoup import BeautifulStoneSoup

class item:
	def __init__(self):
		var.items.append(self)
		
		self.type = None
		self.owner = None
		self.room = None
		
		self.prefix = ''
		self.name = ''
		self.action = ''
		self.place = (0,0)
		self.coords = (0,0)
		self.location = ''
		
		self.container = False
		self.stackable = False
		self.groupable = False
		self.surface = False
		self.chair = False
		
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
		self.place = (-1,-1)
		self.location = 'in %s\'s inventory' % who.name
		
		if self.parent: self.parent.contains.remove(self)
		
		self.parent = None
		who.items.append(self)
	
	def get_room(self):
		return var._c.map[self.coords[0]][self.coords[1]]
	
	def get_room_description(self):
		return self.room_description.replace('%prefix%',self.prefix[0].upper()+self.prefix[1:]).replace('%ref%',self.name)\
			.replace('%action%',words.get_action(self.action)).replace('%pos%',self.location)
	
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

def load_items():
	item_file = open(os.path.join('data','items.xml'),'r')
	soup = BeautifulStoneSoup(item_file)
	item_file.close()
	items = soup.findAll('item')
	
	for _i in items:
		_type = _i.type.renderContents()
		_name = _i.ref.renderContents()
		_prefix = _i.prefix.renderContents()
		_action = _i.action.renderContents()
		
		if _type == 'table':
			_t = table()
			_t.name = _name
			_t.prefix = _prefix
			_t.action = _action
			_t.room_description = _i.room_desc.renderContents()
			_t.description = _i.desc.renderContents()
			
			if _i.surface.renderContents() == 'True':
				_t.surface = True
			else:
				_t.surface = False
		
		elif _type == 'light':
			_t = light()
			_t.name = _name
			_t.prefix = _prefix
			_t.action = _action
			_t.room_description = _i.room_desc.renderContents()
			_t.description = _i.desc.renderContents()

def get_item(type):
	_l = []
	
	for item in var.items:
		if item.type == type:
			_l.append(copy.copy(item))
	
	if _l:
		return _l[functions.random.randint(0,len(_l)-1)]