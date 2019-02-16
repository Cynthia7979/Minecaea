from file_load import *
from articles import *
from mcpi import minecraft

#almost constant variables
lane_width = 24
whr = 2

#chart = main('test.aff')
#notes = chart.get_chart()

#get original point
mc=minecraft.Minecraft.create()
pos=mc.player.getTilePos()
x0, y0, z0 = pos.x, pos.y, pos.z
