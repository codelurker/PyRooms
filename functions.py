#!/usr/bin/python2
import random, time, words, var

def look_for_person(text):
	_p = []
	_r = []
	
	for detail in text:
		detail = detail.lower()
		
		for person in var.player.get_room().guests:
			#Name
			if person.name[0].lower() == detail:
				_p.append(person)
			if person.name[1].lower() == detail:
				_p.append(person)
			
			#Gender
			if person.male and detail in ['man','guy']:
				_p.append(person)
			elif not person.male and detail in ['woman','girl']:
				_p.append(person)
			
			#Description
			for _detail in person.get_visual_description().split(' '):
				_detail = _detail.replace(',','').replace('.','')
				
				if detail == _detail:
					_p.append(person)
		
		#Objects
		for obj in var.player.get_room().objects:
			if obj.name.lower() == detail:
				_p.append(obj)
			
			if obj.place.lower() == detail:
				_p.append(obj)
			
			for _detail in obj.get_description().split(' '):
				_detail = _detail.replace(',','').replace('.','')
				
				if detail == _detail:
					_p.append(obj)
	
	_t = []	
	for p in _p:
		_g = False
		for t in _t:
			if t['person']==p and not _g:
				t['count']+=1
				_g = True
		
		if not _g:
			_t.append({'person':p,'count':0})
	
	count = -1
	for t in _t:
		if t['count'] > count:
			count = t['count']
			_l = [t['person']]
		elif t['count'] == count:
			_l.append(t['person'])
	
	return _l

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

def get_last_name(race):
	random.seed()
	
	if race == 'Human':
		_ret = words.human_lnames[random.randint(0,len(words.human_lnames)-1)]
		words.human_lnames.remove(_ret)
		
		return _ret