#!/usr/bin/python2
import var, words, functions, sys

def parse_input(text):
	if var.interactive:
		text = text.split(' ')
	
	if text[0] in words.commands:
		if text[0] == 'look':
			if len(text) == 1:
				var._c.log(var._c.map[var.player.loc[0]][var.player.loc[1]].get_description())
				
			elif text[1] == 'at' and len(text) > 2:
				_look = functions.look_for_person(text[2:])
					
				if len(_look) > 1:
					var._c.log('There are a number of things here that go by that name:')
					for entry in _look: var._c.log('%s %s,' % (entry.name[0],entry.name[1]))
					print
				elif len(_look):	
					var._c.log(_look[0].get_visual_description())
				else:
					var._c.log('There is nothing here by that description.')
				
			else:
				var._c.log('What are you looking at?')
		
		elif text[0] in ['north','south','east','west','up','down','left','right']:
			if text[0] == 'up':
				text[0] = 'north'
			elif text[0] == 'down':
				text[0] = 'south'
			elif text[0] == 'left':
				text[0] = 'west'
			elif text[0] == 'right':
				text[0] = 'east'
			
			var.player.walk(text[0])
			var._c.tick()
		
		elif text[0] in ['take','pick'] and len(text) >= 2:
			if text[1] == 'up':
				_object = text[2]
			else:
				_object = text[1]
			
			for object in var.player.get_room().objects:
				if object.name == _object:
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
		
		elif text[0] == 'map':
			var._c.draw_map()
		
		elif text[0] == 'talk':
			if text[1] in ['with','to']:
				person = text[2:]
			else:
				person = text[1:]
			
			_look = functions.look_for_person(person)
			
			if len(_look) == 1:
				_person = _look[0]
				var._c.log('You start talking to %s.' % _person.name[0])
				_person.brain.get_dialog_options(var.player)
		
		#var._c.tick()					
	
	elif text[0] in words.attacks:
		#Calculate alignment
		pass
	
	elif text[0] == ord('i') or text[0] == 'i':
		if var.interactive:
			var.interactive = False
			
			#Clear and redraw all windows
			var.window.clear('log')
			var.window.clear('main')
			
			var._c.draw_map()
			return False
		else:
			var.interactive = True
			var.window.clear('log')
			var.window.refresh('log')
			return False
	
	elif text[0] in ['town']:
		if text[0] == 'town' and len(text)==2:
			try:
				print var._c.towns[int(text[1])].get_population()
			except:
				var._c.log('[DEBUG] Town %s does not exist.' % text[1],error=1)
			
	elif text[0] == ord('z'):
		var.camera[1]+=1
		var._c.tick()
	
	else:
		if len(var._c.errors)>1:
			var._c.log('===ERRORS===')
		elif len(var._c.errors)==1:
			var._c.log('===ERROR===')
		
		for error in var._c.errors:
			print error
		
		if var.debug_console:
			print 'Dropping to debugging console...'
			try:
				import code; code.interact(local=locals(),banner='Interactive console launched.')
			except:
				print 'Couldn\'t start an interactive session. You\'re on your own!'
		
		var.running = 0
		return False

def get_input():
	while var.running:
		if var.interactive:
			while not parse_input(var.window.get_str()) == False: pass
		else:
			while not parse_input([var.window.translate(var.window.get_char())]) == False: pass