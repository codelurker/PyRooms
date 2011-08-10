#!/usr/bin/python2

#Developer
debug = False
debug_console = False
running = True
interactive = False
astar_chances = 900
walker_life = 10
camera = [0,0]

#Settings
win_size = (80,25)
world_size = (110,80)
room_size = (25,24)
dungeon_size = (80,80)
offset = (win_size[0]/2)-(room_size[0]/2)
biome_distance = 20
towns = 5
move_ticks = 24

#Stats
base_human_seek_partner_age = 16

#Items
jobs = []
items = []