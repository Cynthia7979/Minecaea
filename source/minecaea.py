import file_load
import articles
import mcpi.minecraft as minecraft

# almost constant variables
lane_width = 24
whr = 2

chart = file_load.load('test.aff')
notes = chart.get_notes()

# get original point
mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()
x0, y0, z0 = pos.x, pos.y, pos.z
