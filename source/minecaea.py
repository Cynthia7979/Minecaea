import file_load
import mcpi.minecraft as minecraft
import mcpi.block as blocks
import numpy as np
from time import sleep

# almost constant variables
LANE_WIDTH = 10
WHR = 2.5  # width-height ratio
DEBUG_OUTPUT = False
Y_SCALE = LANE_WIDTH * 5 / WHR
Z_SCALE = 1e-6
FILE = "0.aff"
CONTINUOUS_ROTATION = False

def mat_product(mat, vec): # for 2*2 mat and 2*n vec
    result=[]
    for v in vec:
        x, z = v[0]*mat[0][0]+v[1]*mat[0][1], v[0]*mat[1][0]+v[1]*mat[1][1]
        v = [x,z]
        result.append(v)
    return result


def main():
    success = True
    # get original point
    mc = minecraft.Minecraft.create()
    pos = mc.player.getTilePos()
    x0, y0, z0 = pos.x, pos.y, pos.z
    rot = mc.player.getRotation()
    if rot <45 or rot >315:
        rotation = [[-1,0],[0,1]]
    elif rot<135:
        rotation = [[0,-1],[-1,0]]
    elif rot<225:
        rotation = [[1,0],[0,-1]]
    else:
        rotation = [[0,1],[1,0]]
        
    theta = rot/360 * 2*np.pi
    if CONTINUOUS_ROTATION == True:
        rotation = [[-np.cos(theta),-np.sin(theta)],[-np.sin(theta),np.cos(theta)]]
    
    music_chart = file_load.load(FILE)
    music_chart.build(LANE_WIDTH, Y_SCALE, Z_SCALE)
    # get last block
    last = music_chart.all_blocks[-1]['z']
    #last_block =  music_chart.t2z(last)[0]
    
    '''
    for i in range(0, 3050, 10):  # Clear space
        mc.setBlocks(x0 - LANE_WIDTH, y0, z0 + i, x0 + 4 + (LANE_WIDTH * 3), y0 + 100, z0 + i + 9, blocks.AIR)
        sleep(0.01)  # Prevent server crash
    '''
    
    mc.setBlock(x0, y0, z0, blocks.WOOL.id, 14)  # Test, also original coordinate
    fl_x0,fl_z0,fl_x1,fl_z1=x0 - LANE_WIDTH,z0,x0 + 4 + (LANE_WIDTH * 3),z0 + last
    floor_coords=[[fl_x0,fl_z0],[fl_x1,fl_z1]]
    floor_coords=mat_product(rotation,floor_coords)
    mc.setBlocks(floor_coords[0][0], y0 - 1, floor_coords[0][1], floor_coords[1][0], y0 - 1, floor_coords[1][1], blocks.IRON_BLOCK)
    '''
    
    lane_border = []
    for i in range(3):
        lane_border=[[x0 + i * LANE_WIDTH + i + 1, z0],[x0 + i * LANE_WIDTH + i + 1, z0 + last_block]]
        lane_border=mat_product(rotation,lane_border)
    '''
    # TODO: mat product for lane borders
    '''
    for i in range(3):
        mc.setBlocks(x0 + i * LANE_WIDTH + i + 1, y0 - 1, z0, x0 + i * LANE_WIDTH + i + 1, y0 - 1, z0 + last, blocks.WOOL, 1)
    '''
    for block in music_chart.all_blocks:
        x, y, z, block_to_set, data = block.values()
        xz = mat_product(rotation, [[x,z]])#x*rotation[0][0]+z*rotation[0][1], x*rotation[1][0]+z*rotation[1][1] # linear algrebra saves me!
        try:
            mc.setBlock(xz[0][0]+x0, y+y0, xz[0][1]+z0, block_to_set.id, data)
        except Exception as e:
            print(e)
            success = False
        if DEBUG_OUTPUT and success:
            print("Setblock at {}, {}, {}".format(x+x0, y+y0, z+z0))
        if not success:
            success = True


if __name__ == '__main__':
    main()
