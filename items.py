#!/usr/bin/python2

class item:
	def __init__(self):
		self.type = None

class light(item):
	def __init__(self):
		item.__init__(self)	
		
		self.type = 'light'