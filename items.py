#!/usr/bin/python2
import functions, words

class item:
	def __init__(self):
		self.type = None
		self.owner = None
	
	def get_room_description(self):
		return self.room_description.replace('%prefix%',self.prefix.upper()).replace('%name%',self.name).replace('%action%',words.get_action(self.action)).replace('%pos%',self.location)

class table(item):
	def __init__(self):
		item.__init__(self)
		
		self.prefix = 'a'
		self.name = 'table'
		self.action = 'sit'
		self.location = 'on the other side of the room'
		self.type = 'table'

class light(item):
	def __init__(self,parent):
		item.__init__(self)
		self.parent = parent
		
		self.prefix = 'a'
		self.name = 'candle'
		self.action = 'burn'
		self.location = '%s %s %s' % (parent.prefix,parent.name,parent.location)
		self.type = 'light'
		
		self.on = True
		
		self.room_description = '%prefix% %name% %action% atop %pos%.'
	
	def get_description(self):
		if self.on:
			return 'Its flame slowly flickers, casting a silent, wavering glow on the %s under it.' % self.parent.name
		

t = table()
l = light(t)

print l.get_room_description()
print l.get_description()