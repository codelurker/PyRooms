#!/usr/bin/python2
import interpreter,people

class room:
	def __init__(self):
		self.name = 'Test'
		self.guests = []


class controller:
	def __init__(self,size=(32,32)):
		self.map = []
		self.size = size
		self.date = [1,0]
		self.ticks = 0
		self.people = []
		
	def generate(self):
		print 'Making world',
	
		for x in range(self.size[0]):
			print '.',
			ycols = []
			
			for y in range(self.size[1]-1):
				ycols.append(room())
			
			self.map.append(ycols)
		
		print 'Done!\n',
	
	def make_human_race(self):
		adam = people.human()
		adam.name = ('Adam','')
		adam.age = 30
		adam.strength = 6
		adam.dexterity = 4
		adam.intelligence = 6
		adam.charisma = 6
		
		eve = people.human()
		eve.name = ('Eve','')
		eve.male = False
		eve.age = 25
		eve.strength = 4
		eve.dexterity = 5
		eve.intelligence = 3
		eve.charisma = 8
		
		adam.marry(eve)
		
		for _r in range(2,people.random.randint(4,5)):
			eve.impregnate(adam)
		
	def tick(self,ticks = 1):
		print 'Ticking',
		
		for _t in range(ticks):
			print '.',
			self.ticks += _t
			
			if self.ticks == 1440:
				self.date[1]+=1
				self.ticks = 0
		
		print 'Done!\n',
	
	def tick_year(self,amnt):
		if amnt == 1:
			print '[Time] Advancing 1 year.'
		else:
			print '[Time] Advancing %s years.' % amnt
		
		for _y in range(14400*amnt):
			for _p in self.people:
				_p.tick()
			
			self.ticks += 1
			
			if self.ticks/48 > self.date[0]:
				self.date[0]+=1
			
			if self.ticks == 14400:
				self.date[0]=1
				self.date[1]+=1
				self.ticks = 0
				
				#print '[Time] It is now year %s.' % self.date[1]
				
				for _p in self.people:
					_p.events['lastbirthday']=False