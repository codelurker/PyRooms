#!/usr/bin/python2
import controller, items, var, interpreter, words
if var.debug: import time

var._c = controller.controller()
items.load_items()
words.load_room_descriptions()
words.load_phrases()

if var.debug: _starttime = time.time()

var._c.generate()
var._c.make_human_race()
#var._c.tick_year(40)

if var.debug: print 'Generation took %s' % (str(time.time()-_starttime))

interpreter.get_input()