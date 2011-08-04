#!/usr/bin/python2
import var, items, jobs, os, sys, random, json, xml2json, hashlib

random.seed()

def opposite(text):
	if text == 'north':
		return 'south'
	elif text == 'south':
		return 'north'
	elif text == 'east':
		return 'west'
	elif text == 'west':
		return 'east'

def cut_text(text,detail):
	parts = text.split('|')
	if detail > len(parts) :
		detail = len(parts)
	
	if detail:
		return ''.join(parts[:detail])+''
	else:
		return ''

light_filler = ['the floor below it','the walls around it']
def get_desc_light_filler(obj):
	return light_filler[random.randint(0,len(light_filler)-1)]

room_description_poor_lighting = ['The room is very dark|, and your eyes take a moment to adjust to the dim light']
def get_desc_lighting(lights):
	if lights in [1,2]:
		_ret = room_description_poor_lighting[random.randint(0,len(room_description_poor_lighting)-1)]
		return cut_text(_ret,lights)
	
	elif not lights:
		return 'It is too dark to see anything'
	
	elif lights >= 3:
		if var.debug: return '<FIXME> Not enough lighting phrases for %s lights.' % lights
		return None

def get_desc_interior(type,lights):
	_l = []
	
	for key in interior_descriptions:
		if key['type'] == type:
			_l.append(key['desc'])
	
	if type == 'stone':
		_ret = _l[random.randint(0,len(_l)-1)]
		return cut_text(_ret,lights)
	else:
		return None

def get_desc_outside(type,lights):
	_l = []
	
	for key in outside_descriptions:
		if key['type'] == type:
			_l.append(key['desc'])
	
	_ret = _l[random.randint(0,len(_l)-1)]
	return cut_text(_ret,lights)

def get_phrase(type):
	_l = []
	
	for entry in phrases:
		if entry['type'] == type:
			_l.append(entry['text'])
	
	return _l[random.randint(0,len(_l)-1)]

interior_descriptions = []
outside_descriptions = []
human_male_fnames = []
human_female_fnames = []
human_lnames = []
phrases = []
def load_config_files(flush=False):
	_f = open(os.path.join('data','config_files.txt'),'r')
	_flist = _f.readlines()
	_f.close()
	
	try:
		_f = open(os.path.join('data','hashes.txt'),'r')
	except:
		_f = open(os.path.join('data','hashes.txt'),'w')
		_f.write('')
		_f.close()
		_f = open(os.path.join('data','hashes.txt'),'r')
	
	_fhashes = _f.readlines()
	_f.close()
	
	_newhashes = []
	for file in _flist:
		
		file = file[:len(file)-1]+'.xml'
		_t = open(os.path.join('data',file),'r')
		_newhashes.append((file,hashlib.md5(_t.read()).hexdigest()))
		_t.close()
	
	_hashes = []
	for hash in _fhashes:
		if flush:
			_h = hash[:len(hash)-1]+'derp'
		else:
			_h = hash[:len(hash)-1]
		_hashes.append(tuple(_h.split(',')))
	
	aa = set(_newhashes)
	bb = set(_hashes)
	
	if aa.difference(bb):
		if var.debug: print 'CONVERTAN'
		for file in aa.difference(bb):
			_ret = xml2json.parse(os.path.join('data',file[0]),debug=True)
			
			for i in range(0,len(_hashes)):
				if _hashes[i][0] == file[0]:
					_hashes[i] = file
		
		_f = open(os.path.join('data','hashes.txt'),'w')
		for file in _hashes:
			_f.write('%s,%s\n' % (file[0],file[1]))
		_f.close()
	
	for file in _flist:
		file = file[:len(file)-1]
		if var.debug: print 'Loading '+file
		try:
			_f = open(os.path.join('data',file+'.json'))
		except:
			print 'ERROR: Some of your .JSON files are broken.\n'
			print 'This could happen if you haven\'t compiled your .XML files yet.'
			print 'Run: ./main.py recompile'
			sys.exit()
		
		
		for line in _f.readlines():
			_j = json.loads(line)
			
			for _key in _j.iterkeys():
				key = _key
				break

			if file == 'descriptions':
				if key.count('interior'):
					global interior_descriptions
					interior_descriptions.append({'type':key[len('interior-'):],'desc':_j[key]})
				elif key.count('outside'):
					global outside_descriptions
					outside_descriptions.append({'type':key[len('outside-'):],'desc':_j[key]})
			
			elif file == 'phrases':
				global phrases
				phrases.append({'type':key,'text':_j[key]})
			
			elif file == 'names':
				if key == 'male':
					global human_male_fnames
					human_male_fnames = _j[key].split(',')
				elif key == 'female':
					global human_female_fnames
					human_female_fnames = _j[key].split(',')
				elif key == 'last':
					global human_lnames
					human_lnames = _j[key].split(',')
			
			elif file == 'jobs':
				_i = jobs.job(_j['name'])
				_i.strength_needed = int(_j['strength'])
				_i.dexterity_needed = int(_j['dexterity'])
				_i.intelligence_needed = int(_j['intelligence'])
			
			elif file == 'items':
				if _j['type'] == 'light':
					_i = items.light()
				elif _j['type'] == 'table':
					_i = items.table()
				elif _j['type'] == 'foliage':
					_i = items.foliage()
				elif _j['type'] == 'window':
					_i = items.window()
				elif _j['type'] == 'clothing':
					_i = items.clothing()
					_i.madeof = _j['madeof']
					_i.slot = _j['slot']
					
				_i.name = _j['ref']
				_i.prefix = _j['prefix']
				_i.action = _j['action']
				_i.room_description = _j['room_desc']
				_i.description = _j['desc']
				_i.weight = _j['weight']
		
		_f.close()

commands = ['look','ask','north','south','east','west','up','down','left','right','take','pick','drop','items','put','talk','map']
attacks = ['stab', 'punch', 'kick']
body_parts = ['head','eyes', 'larm','rarm','lhand','rhand','chest','stomach','torso','groin','lleg','rleg','lfoot','rfoot']