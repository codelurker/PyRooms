#!/usr/bin/python2
import controller, items, var, interpreter

var._c = controller.controller()
items.load_items()
var._c.generate()
var._c.make_human_race()
print var._c.map[0][0].get_description()
#var._c.tick_year(1)
#interpreter.get_input()