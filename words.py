#!/usr/bin/python2
import os, random, xml2json, var, hashlib
from BeautifulSoup import BeautifulStoneSoup

random.seed()

def read_word_list(fname):
	_r = open(os.path.join('data',fname),'r')
	return sorted(_r.readlines()[0].split(','))
	_r.close()

def get_action(word):
	for _keyword in keywords:
		if word == _keyword[0]:
			return _keyword[1]

def cut_text(text,detail):
	parts = text.split('|')
	if detail > len(parts) :
		detail = len(parts)
	
	if detail:
		return ''.join(parts[:detail])+'.'
	else:
		return ''

light_filler = ['the floor below it','the walls around it']
def get_desc_light_filler(obj):
	return light_filler[random.randint(0,len(light_filler)-1)]

def get_desc_location(obj):
	if obj.coords == (0,0):
		return 'in the northwest corner of the room'

room_description_poor_lighting = ['The room is very dark|, and your eyes take a moment to adjust to the dim light']
def get_desc_lighting(lights):
	if lights in [1,2]:
		_ret = room_description_poor_lighting[random.randint(0,len(room_description_poor_lighting)-1)]
		return cut_text(_ret,lights)
	
	elif not lights:
		return 'It is too dark to see anything.'
	
	elif lights >= 3:
		if var.debug: return '<FIXME> Not enough lighting phrases for %s lights.' % lights
		return None

def get_desc_interior(type,lights):
	if type == 'stone':
		_ret = room_description_interior_stone[random.randint(0,len(room_description_interior_stone)-1)]
		return cut_text(_ret,lights)
	else:
		return ''

def get_phrase(type):
	_l = []
	
	for entry in phrases:
		if entry['type'] == type:
			_l.append(entry['text'])
	
	return _l[random.randint(0,len(_l)-1)]

room_description_interior_stone = []
room_description_interior_stone_wet = []
def load_room_descriptions():
	room_desc_file = open(os.path.join('data','room_interior_descriptions.xml'),'r')
	soup = BeautifulStoneSoup(room_desc_file)
	room_desc_file.close()
	_stone = soup.findAll('stone')
	
	for _i in _stone:
		room_description_interior_stone.append(_i.renderContents())

phrases = []
def load_phrases():
	phrase_file = open(os.path.join('data','phrases.xml'),'r')
	soup = BeautifulStoneSoup(phrase_file)
	phrase_file.close()
	
	_room_exit = soup.findAll('room_exit')
	_introduction = soup.findAll('introduction')
	
	for _i in _room_exit:
		phrases.append({'type':'room_exit','text':_i.renderContents()})
	
	for _i in _introduction:
		phrases.append({'type':'introduction','text':_i.renderContents()})

def load_config_files(flush=False):
	_f = open(os.path.join('data','config_files.txt'),'r')
	_flist = _f.readlines()
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
		for file in aa.difference(bb):
			_ret = xml2json.parse(os.path.join('data',file[0]),debug=True)
			
			for i in range(0,len(_hashes)):
				if _hashes[i][0] == file[0]:
					_hashes[i] = file
		
		_f = open(os.path.join('data','hashes.txt'),'w')
		for file in _hashes:
			_f.write('%s,%s\n' % (file[0],file[1]))
		_f.close()
		

load_config_files(flush=False)

commands = ['look','ask','north','south','east','west','take','drop','items','put','talk']
attacks = ['stab', 'punch', 'kick']
body_parts = ['head','eyes', 'larm','rarm','lhand','rhand','chest','stomach','torso','groin','lleg','rleg','lfoot','rfoot']