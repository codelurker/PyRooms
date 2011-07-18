#!/usr/bin/python2
import functions, words, var, os
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
		self.location = '' #on the other side of the room
		
	def sanitize(self,text,tag):
		return text.rpartition(tag)[0].split('|')[0]+' '+words.get_desc_light_filler(self)+'.'
	
	def get_room_description(self):
		return self.room_description.replace('%prefix%',self.prefix.upper()).replace('%ref%',self.name).replace('%action%',words.get_action(self.action)).replace('%pos%',self.location)

class container(item):
	def __init__(self):
		item.__init__(self)
		
		self.type = 'container'
		
		#what, where
		self.contains = []
	
	def put(self,item,where):
		self.contains.append({'item':item,'where':where})

class light(item):
	def __init__(self):
		item.__init__(self)
		self.parent = None
		
		#self.location = '%s %s %s' % (parent.prefix,parent.name,parent.location)
		self.type = 'light'
		
		self.on = True
		
		#self.room_description = ''
	
	def get_description(self):
		if self.on:
			if self.parent:
				return self.description.replace('%parent%',self.parent.name)
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
		
		if _type == 'container':
			_t = container()
			_t.name = _name
			_t.prefix = _prefix
			_t.action = _action
		
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
			_l.append(item)
	
	return _l[functions.random.randint(0,len(_l)-1)]