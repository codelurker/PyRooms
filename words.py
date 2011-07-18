#!/usr/bin/python2
import os, random

random.seed()

hmf = open(os.path.join('data','human_male_fnames.txt'),'r')
human_male_fnames = sorted(hmf.readlines()[0].split(','))
hmf.close()

hff = open(os.path.join('data','human_female_fnames.txt'),'r')
human_female_fnames = sorted(hff.readlines()[0].split(','))
hff.close()

hln = open(os.path.join('data','human_lnames.txt'),'r')
human_lnames = sorted(hln.readlines()[0].split(','))
hln.close()

_keywords = open(os.path.join('data','keywords.txt'),'r')
__keywords = sorted(_keywords.readlines()[0].split(','))
keywords = []
for key in __keywords:
	keywords.append(key.split(':'))
	
_keywords.close()

commands = ['look','ask']

def get_action(word):
	for _keyword in keywords:
		if word == _keyword[0]:
			return _keyword[1]

def cut_text(text):
	parts = text.split('|')
	return ''.join(parts[:random.randint(1,len(parts))])+'.'

light_filler = ['the floor below it','the walls around it']
def get_desc_light_filler(obj):
	return light_filler[random.randint(0,len(light_filler)-1)]

random_location = ['in the far corner','next to the door']
def get_desc_random_location():
	return random_location[random.randint(0,len(random_location)-1)]

room_description_poor_lighting = ['The room is very dark|, and your eyes take a moment to adjust to the dim light.']
def get_desc_lighting(lights,detail):
	if lights == 1:
		if detail:
			return room_description_poor_lighting[random.randint(0,len(room_description_poor_lighting)-1)].replace('|','')
		else:
			return room_description_poor_lighting[random.randint(0,len(room_description_poor_lighting)-1)].split('|')[0]+'.'

room_description_interior_stone = ['A brief glance at the interior reveals that the walls are composed of light-grey stone| stacked one upon the other|, padded with wooden slabs every few feet']
room_description_interior_stone_wet = ['']
def get_desc_interior(type):
	if type == 'stone':
		_ret = room_description_interior_stone[random.randint(0,len(room_description_interior_stone)-1)]
		return cut_text(_ret)