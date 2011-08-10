#Cursed is a wrapper for Python's Curses module
#By default, Python for Windows doesn't support
#Curses. However, it can be downloaded here:
#http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
#
#Cursed was created by Luke Martin (flags)
#This program is free software. It comes without any warranty, to
#the extent permitted by applicable law. You can redistribute it
#and/or modify it under the terms of the Do What The Fuck You Want
#To Public License, Version 2, as published by Sam Hocevar. See
#http://sam.zoy.org/wtfpl/COPYING for more details.
import sys

try:
	import curses
except:
	print 'This terminal/version of Python doesn\'t support curses.'
	print 'If you are on Windows, download curses-2.2 from'
	print 'http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses'
	sys.exit()

class cursed:
	def __init__(self):
		self.screen = [{'name':'main','win':curses.initscr(),'pad':False}]

		#Screen
		curses.noecho()
		curses.cbreak()
		self.screen[0]['win'].keypad(1)
		curses.curs_set(0)
		
		#Colors
		if curses.has_colors:
			curses.start_color()
			self.color = 1
			curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
			curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
			curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
			curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
			curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
			curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
			curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_WHITE)
			curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_CYAN)
	
	def set_color(self,i):
		self.color = i
	
	def create_window(self,name,spos,epos,pad=False):
		width = epos[0]-spos[0]
		height = epos[1]-spos[1]
		
		win = curses.newwin(height, width, spos[1], spos[0])
		
		if pad:
			self.screen.append({'name':name,'win':win,'spos':spos,'epos':epos,'pad':True,'log':['' for i in range(height)],'height':height-1})
		else:
			self.screen.append({'name':name,'win':win,'spos':spos,'epos':epos,'pad':False})
	
	def translate(self,text):
		if text == curses.KEY_LEFT:
			return 'left'
		elif text == curses.KEY_RIGHT:
			return 'right'
		elif text == curses.KEY_UP:
			return 'up'
		elif text == curses.KEY_DOWN:
			return 'down'
		else:
			return text
	
	def get_height(self,name):
		for screen in self.screen:
			if screen['name'] == name:
				return screen['height']
	
	def get_char(self):
		return self.screen[0]['win'].getch()
	
	def get_str(self):
		curses.nocbreak();
		curses.echo();
		self.screen[0]['win'].addstr(24,0, '> ')
		curses.curs_set(1)
		s = self.screen[0]['win'].getstr();
		curses.curs_set(0)
		self.clear_line(24)
		curses.noecho();
		curses.cbreak();
		
		return s
	
	def clear(self,name):
		for screen in self.screen:
			if screen['name'] == name:
				screen['win'].clear()
				
	def refresh(self,name):
		for screen in self.screen:
			if screen['name'] == name:
				screen['win'].refresh()

	def clear_line(self,line,char=' '):
		for i in range(0,79):
			try: self.screen[0]['win'].addstr(line,i, char)
			except: pass
	
	def write(self,name,text,pos):
		for screen in self.screen:
			if screen['name'] == name:
				try:
					screen['win'].addstr(pos[1]-1,pos[0], text, curses.color_pair(self.color))
				except:
					pass
				
				return True
	
	def write_append(self,name,text):
		for screen in self.screen:
			if screen['name'] == name and screen['pad']:
				screen['win'].clear()
				screen['log'].pop(0)
				screen['log'].append(text)
				
				try:
					for i in range(0,screen['height']):
						screen['win'].addstr(screen['height']-i,0, screen['log'][screen['height']-i])
				except:
					pass
				
				return True
	
	def end(self):
		curses.nocbreak();
		self.screen[0]['win'].keypad(0);
		curses.echo()
		curses.endwin()