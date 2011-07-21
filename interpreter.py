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
	
	else:
		return False
				

def get_input():
	while not parse_input(raw_input('> ')) == False: pass
	