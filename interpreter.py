#!/usr/bin/python2
import words,random,time,var

def get_date():
	return list(var._c.date)

def get_ticks():
	return int(var._c.ticks)

def get_future_date(ticks):
	_d = get_date()
	_t = get_ticks()
	__t = _t
	
	
	for t in range(ticks):
		_t += 1

		if _t/48 > _d[0]:
			_d[0]+=1
	
		if _t == 14400:
			_d[0]=1
			_d[1]+=1
			_t = 0
	
	return _d

def get_name(race,male):
	random.seed()
	
	if male:
		if race == 'Human':
			return words.human_male_fnames[random.randint(0,len(words.human_male_fnames)-1)]
	
	else:
		if race == 'Human':
			return words.human_female_fnames[random.randint(0,len(words.human_female_fnames)-1)]