import file_load
import articles
import mcpi.minecraft as minecraft
import mcpi.block as block

# almost constant variables
lane_width = 24
whr = 2

chart = file_load.load('test.aff')
notes = chart.get_notes()

# get original point
mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()
x0, y0, z0 = pos.x, pos.y, pos.z
mc.setBlock(x0, y0, z0, block.STONE)  # Test


def main():
    music_chart = file_load.load("test.aff")
    music_chart.build()
