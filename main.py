#!/usr/bin/python2
import controller, var, interpreter

var._c = controller.controller()
var._c.generate()
var._c.make_human_race()
#ar._c.tick_year(10)
interpreter.get_input()