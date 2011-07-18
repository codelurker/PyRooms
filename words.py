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

light_filler = ['the floor below it','the walls around it']
def get_desc_light_filler(obj):
	return light_filler[random.randint(0,len(light_filler)-1)]

random_location = ['in the far corner','next to the door']
def get_desc_random_location():
	return random_location[random.randint(0,len(random_location)-1)]