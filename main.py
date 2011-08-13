#!/usr/bin/python2
import controller, functions, items, var, interpreter, words, sys
if var.debug: import time
import cursed

var.window = cursed.cursed()
var.window.create_window('log',(26,1),(80,16))
var.window.create_window('status',(0,24),(79,25),pad=True)
var.window.create_window('health',(26,16),(79,17),pad=True)

var._c = controller.controller()

if len(sys.argv)>1 and sys.argv[1] == 'recompile':
	words.load_config_files(flush=True)
else:
	words.load_config_files(flush=False)

if var.debug: _starttime = time.time()

var._c.generate()
var._c.make_human_race()
#var._c.tick(300)
#var._c.tick_year(1)

if var.debug: print 'Generation took %s' % (str(time.time()-_starttime))

var._c.log('')
var.window.clear('log')
var.window.refresh('log')
var._c.draw_map()

var.window.refresh('log')
interpreter.get_input()
var.window.end()