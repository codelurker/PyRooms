#!/usr/bin/python2
import words,random,time,var

def get_date():
	print 'derp'
	return var._c.date
	#time.strftime('[%m-%d-%Y - %I:%M %p]')

def get_name(race,male):
	random.seed()
	
	if male:
		if race == 'Human':
			return words.human_male_fnames[random.randint(0,len(words.human_male_fnames)-1)]