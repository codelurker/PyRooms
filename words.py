#!/usr/bin/python2
import os

hmf = open(os.path.join('data','human_male_fnames.txt'),'r')
human_male_fnames = sorted(hmf.readlines()[0].split(','))
hmf.close()

hff = open(os.path.join('data','human_female_fnames.txt'),'r')
human_female_fnames = sorted(hff.readlines()[0].split(','))
hff.close()