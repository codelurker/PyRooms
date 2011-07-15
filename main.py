#!/usr/bin/python2
import controller, var

var._c = controller.controller()
var._c.generate()
var._c.make_human_race()
var._c.tick_year(3)