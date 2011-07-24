#!/usr/bin/python2
import var, words, functions, sys

def parse_input(text):
	text = text.split(' ')
	
	if text[0] in words.commands:
		if text[0] == 'look':
			if len(text) == 1:
				print var._c.map[var.player.place[0]][var.player.place[1]].get_description()
				
			elif text[1] == 'at' and len(text) > 2:
				_look = functions.look_for(text[2])
				
				if len(_look) > 1:
					var._c.log('There are a number of things here that go by that name:')
					for entry in _look: var._c.log('%s %s,' % (entry.name[0],entry.name[1]))
					print
				elif len(_look):
					var._c.log('%s looks very good!' % (_look[0].name[0]))
				else:
					var._c.log('There is nothing here by that name!')
				
			else:
				var._c.log('What are you looking at?')
		
		elif text[0] in ['north','south','east','west']:
			var.player.walk(text[0])
		
		elif text[0] == 'take' and len(text) == 2:
			for object in var.player.get_room().objects:
				if object.name == text[1]:
					object.take(var.player)
					var._c.log('You take the %s.' % object.name)
					break
		
		elif text[0] == 'drop' and len(text) == 2:
			for item in var.player.items:
				if item.name == text[1]:
					var.player.items.remove(item)
					var.player.get_room().add_object(item)
					var._c.log('You drop the %s.' % item.name)
					break
		
		elif text[0] == 'put' and len(text) > 2:
			for item in var.player.items:
				if item.name == text[1]:
					_item = item					
					break
			
			for object in var.player.get_room().objects:
				if text[2] == 'on':
					if object.name == text[3] and object.surface:
						var.player.items.remove(_item)
						var.player.get_room().add_object(_item)
						_item.sit_on(object)
						var._c.log('You put the %s on the %s.' % (_item.name,object.name))
						break
		
		elif text[0] == 'items':
			if len(var.player.items):
				var._c.log('In your inventory:')
			else:
				var._c.log('You are carrying nothing.')
			
			_items = []
			for item in var.player.items:
				for _item in _items:
					if _item['name'] == item.name:
						_item['count'] += 1
				else:
					_items.append({'name':item.name,'count':1,'obj':item})
					
				_t = []
			
			for item in _items:
				if not item['name'] in _t:
					if item['count'] > 1:
						var._c.log('%s (x%s)' % (item['obj'].name,item['count']))
						_t.append(item['name'])
					else:
						var._c.log(item['obj'].name)
	
	elif text[0] in words.attacks:
		#Calculate alignment
		pass
	
	else:
		return False
				

def get_input():
	while not parse_input(raw_input('> ')) == False: pass
	