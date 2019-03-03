import file_load
import articles
import mcpi.minecraft as minecraft
import mcpi.block as blocks

# almost constant variables
lane_width = 10
whr = 2  # width-height ratio
DEBUG_OUTPUT = True
y_scale = lane_width * 4 / whr
z_scale = 10**(-4)


def main():
    success = True
    # get original point
    mc = minecraft.Minecraft.create()
    pos = mc.player.getTilePos()
    x0, y0, z0 = pos.x, pos.y, pos.z
    mc.setBlock(x0, y0, z0, blocks.WOOL.id, 3)  # Test, also original coordinate
    mc.setBlocks(x0-7, y0-1, z0, x0+(lane_width*4), y0-1, z0+10000, blocks.IRON_BLOCK)
    music_chart = file_load.load("0.aff")
    music_chart.build(lane_width, y_scale, z_scale)
    print("CHART: \n", music_chart)
    for block in music_chart.all_blocks:
        x, y, z, block_to_set, data = block.values()
        try:
            mc.setBlock(x+x0, y+y0, z+z0, block_to_set.id, data)
        except:
            print('I ????????????')
            success = False
        if DEBUG_OUTPUT and success:
            print("Setblock at {}, {}, {}".format(x+x0, y+y0, z+z0))
        if not success:
            success = True


if __name__ == '__main__':
    main()
