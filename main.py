#!/usr/bin/python2
import controller, functions, items, var, interpreter, words, sys
if var.debug: import time
import cursed

var.window = cursed.cursed()
var.window.create_window('log',(0,19),(79,24),pad=True)

var._c = controller.controller()

if len(sys.argv)>1 and sys.argv[1] == 'recompile':
	words.load_config_files(flush=True)
else:
	words.load_config_files(flush=False)

if var.debug: _starttime = time.time()

var._c.generate()
var._c.make_human_race()
#var._c.tick(300)
var._c.tick_year(1)

if var.debug: print 'Generation took %s' % (str(time.time()-_starttime))

var.window.clear('log')
var.window.refresh('log')
var._c.draw_map()
#var._c.log(str(var.window.get_height('log')))
var.window.refresh('log')
interpreter.get_input()
var.window.end()