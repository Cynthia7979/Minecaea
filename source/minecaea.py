import file_load
import articles
import mcpi.minecraft as minecraft
import mcpi.block as blocks

# almost constant variables
lane_width = 24
whr = 2


def main():
    # get original point
    mc = minecraft.Minecraft.create()
    pos = mc.player.getTilePos()
    x0, y0, z0 = pos.x, pos.y, pos.z
    mc.setBlock(x0, y0, z0, blocks.WOOL.id, 3)
    music_chart = file_load.load("test.aff")
    music_chart.build(lane_width, 50, 0.1)
    for block in music_chart.all_blocks:
        x, y, z, block, data = block.values()
        mc.setBlock(x+x0, y+y0, z+z0, block, data)


if __name__ == '__main__':
    main()
