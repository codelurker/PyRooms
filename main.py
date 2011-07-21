#!/usr/bin/python2
import controller, items, var, interpreter, words

var._c = controller.controller()
items.load_items()
words.load_room_descriptions()
words.load_phrases()
var._c.generate()
var._c.make_human_race()
#print var._c.map[0][0].get_description()
#var._c.tick_year(1)
interpreter.get_input()