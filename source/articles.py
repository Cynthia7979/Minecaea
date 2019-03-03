# -*- coding: gb2312 -*-

import mcpi.block as block
import numpy as np

"""
Minecaea - Minecraft version of Arcaea
class structure
============================

x-axis: int
    leftmost = -50
    rightmost = 150
    center = 50

y-axis: int
    uppermost = 100 (sky tap line)
    bottommost = -1 (floor)
    center = 50

lane: int
    leftmost = 1
    rightmost = 4

color: int
    0 = blue
    1 = red

notes: tuple of int, representing time in ms

block: tuple (block, data)
    block: block instance from mcpi.block
    data: int, representing block's kind (s.a. saplings, wools, stained glass, etc.)

x y t AND x y z coordinates: Arcaea and Minecraft coordinates

"""


class Article(object):  # For "物件", renamed "article" because of collision with "object"
    keyword = None

    def __init__(self):
        self.t1 = None

    def check_class(self, other):  # Syntactic sugar
        assert isinstance(other, Article), "{} is not an instance of Article".format(other)

    def __gt__(self, other):
        self.check_class(other)
        return self.t1 > other.t1

    def __ge__(self, other):
        self.check_class(other)
        return self.t1 >= other.t1

    def __eq__(self, other):
        self.check_class(other)
        return self.t1 == other.t1

    def __str__(self):
        return "Article instance at {time}ms.".format(time=self.t1)


class Note(Article):
    _block = ((block.AIR, None), )

    def __init__(self):
        super().__init__()
        self.t1, self.t2, \
        self.x1, self.x2, \
        self.y1, self.y2 = (None,) * 6
        self.block = self.__class__._block[0]

    def get_blocks(self, x_scale, y_scale, z_scale):
        pass

    def __str__(self):
        return "{name} instance at {start_time}~{end_time}ms with pos x ({start_x}~{end_x}), y({start_y}~{end_y})".\
            format(
                name=self.__class__.__name__,
                start_time=self.t1, end_time=self.t2,
                start_x=self.x1, end_x=self.x2,
                start_y=self.y1, end_y=self.y2
            )


class FloorNote(Note):
    def __init__(self, t1, t2, lane):
        super().__init__()
        self.x1, self.x2 = (int(lane), int(lane))
        self.y1, self.y2 = (0, 0)
        self.t1, self.t2 = int(t1), int(t2)


class FloorTap(FloorNote):
    keyword = ""
    _block = ((block.WOOL, 9), )

    def __init__(self, t, lane):
        super().__init__(t, t, lane)
        self.block = self.__class__._block[0]
        self.visual_length = 4  # visual width in blocks

    def get_blocks(self, lane_width, y_scale, z_scale):
        block_list = []
        for i in range(self.visual_length):
            for n in range(lane_width):
                #                  |---------------x--------------|   y  z     block
                block_list.append([(self.x1-1) * (lane_width +1) - n, -1, i, self.block])
        return block_list


class FloorHold(FloorNote):
    keyword = "hold"
    _block = ((block.WOOL, 9), )

    def __init__(self, t1, t2, lane):
        super().__init__(t1, t2, lane)
        self.block = self.__class__._block[0]

    def get_blocks(self, lane_width, y_scale, z_scale):  # pls pass chart.z_scale*bpm as z_scale
        block_list = []
        for i in range(int(z_scale * (self.t2 - self.t1))):
            for n in range(lane_width):
                #                  |---------------x---- -------|   y  z     block
                block_list.append([(self.x1-1) * (lane_width +1) - n, -1, i, self.block])
        return block_list


class SkyNote(Note):
    keyword = "arc"

    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod):
        super().__init__()
        self.t1, self.t2 = int(t1), int(t2)
        self.x1, self.x2 = float(x1), float(x2)
        self.y1, self.y2 = float(y1), float(y2)
        self.slidemethod = slidemethod

    def get_curve(self, lane_width, y_scale, z_scale):
        # returns coordinates of the centre of the curve, z_scale is bpm*z_scale
        block_list = []
        t = 0
        x0, y0, z0 = self.x1*lane_width*2, self.y1*y_scale, 0
        x1, y1, z1 = self.x2*lane_width*2, self.y2*y_scale, (self.t2 - self.t1) * z_scale
        dx = x1 - x0  # d = delta
        dy = y1 - y0
        dz = int(z1)
        step = 1 / (abs(dx) + abs(dy) + dz +1)

        if self.slidemethod == 's':
            while t <= 1:
                block = (x0+t*dx, y0+t*dy, z0+t*dz)
                block_list.append(block)
                t += step
        elif self.slidemethod == 'b':
            for i in range(dz+1):
                l = i / dz
                x = x0 + dx * -2 * l * l * (l - 1.5)
                y = y0 + dy * -2 * l * l * (l - 1.5)
                block = (x, y, i)
                block_list.append(block)
        else:  # Prototype
            x_list = []
            y_list = []
            z_list = []
            for i in range(dz):
                z_list.append(i/dz)
            slidemethod = self.slidemethod

            try:
                if slidemethod[3] == 'i':  # sisi, sosi
                    for i in z_list:
                        y_list.append(np.sin(i*np.pi/2))
                else:
                    for i in z_list:
                        y_list.append(-np.cos(i*np.pi/2)+1)

            except IndexError:  # exception oriented programming
                y_list = z_list

            if slidemethod[1] == 'i':  # sisi, siso
                for i in z_list:
                        x_list.append(np.sin(i*np.pi/2))
            else:
                for i in z_list:
                        x_list.append(-np.cos(i*np.pi/2)+1)

            for i in range(dz):
                block_list.append((x0+dx*x_list[i],y0+dy*y_list[i],i))
        return block_list
    

class Arc(SkyNote):
    _block = ((block.STAINED_GLASS, 3), (block.STAINED_GLASS, 14))

    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod, color):
        super().__init__(t1, t2, x1, x2, y1, y2, slidemethod)
        self.block = self.__class__._block[int(color)]
        self.size = 3

    def __str__(self):
        return "{name} instance at {start_time}~{end_time}ms with pos x ({start_x}~{end_x}), y({start_y}~{end_y})," \
               " slidemethod={slidemethod} and color={color}".\
            format(
                name=self.__class__.__name__,
                start_time=self.t1, end_time=self.t2,
                start_x=self.x1, end_x=self.x2,
                start_y=self.y1, end_y=self.y2,
                slidemethod=self.slidemethod, color=self.block
            )

    def get_blocks(self, lane_width, y_scale, z_scale):  # TODO: reduce computation
        block_list=[]
        trace = self.get_curve(lane_width, y_scale, z_scale)
        for p in trace:
            for w in range(-self.size,self.size):
                for h in range(self.size - abs(w)):
                    for l in range(self.size - abs(w) - h):      # 66666666
                        block_list.append((
                            p[0] + w,
                            p[1] + h,
                            p[2] + l,
                            self.block
                            ))
        return block_list


class SkyLine(SkyNote):
    _block = ((block.STAINED_GLASS, 2), )

    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod, notes):
        super().__init__(t1, t2, x1, x2, y1, y2, slidemethod)
        self.notes = [int(note) for note in notes]
        self.visual_size = [8, 2, 2]  # width, height, length
        self.block = self.__class__._block[0]

    def __str__(self):
        return "{name} instance at {start_time}~{end_time}ms with pos x ({start_x}~{end_x}), y({start_y}~{end_y})," \
               " slidemethod={slidemethod}. Notes are: {notes}".\
            format(
                name=self.__class__.__name__,
                start_time=self.t1, end_time=self.t2,
                start_x=self.x1, end_x=self.x2,
                start_y=self.y1, end_y=self.y2,
                slidemethod=self.slidemethod, notes=self.notes
            )
    
    def get_blocks(self, lane_width, y_scale, z_scale):
        block_list = []
        trace = self.get_curve(lane_width, y_scale, z_scale)
        for p in trace:
            block_list.append((p[0], p[1], p[2], self.block))  # TODO: add self.block for trace & skytaps
        for note in self.notes:
            z = int(
                z_scale*(self.t2-self.t1) * ((note-self.t1) / (self.t2-self.t1))
            )
            try:
                centre = trace[z]
            except IndexError:
                print((z,len(trace)))
                print('centre location error at '+str(note))
                centre = trace[-1]
            for w in range(self.visual_size[0]):
                for h in range(self.visual_size[1]):
                    for l in range(self.visual_size[2]):
                        block_list.append((
                            centre[0]+w-self.visual_size[0]/2,
                            centre[1]+h-self.visual_size[1]/2,
                            centre[2]+l-self.visual_size[2]/2,
                            self.block
                            ))
        return block_list


class Timing(Article):
    keyword = "timing"

    def __init__(self, time, bpm, beat):
        super().__init__()
        self.t1 = int(time)
        self.bpm = float(bpm)
        self.beat = float(beat)

    def __str__(self):
        return "Timing instance at {time}ms with bpm {bpm} and beat {beat}".\
            format(
                time=self.t1,
                bpm=self.bpm,
                beat=self.beat
            )


class Chart(object):
    def __init__(self):
        self.offset = None
        self._notes = []
        self._lanewidth = 25
        self._whr = 2  # width-height ratio
        self._timings = []
        self._chart = []
        self.z_scale = 1
        self.all_blocks = []
        
    def add_note(self, note):
        if isinstance(note, Note):  # If it isn't a blank line, comment or something
            self._notes.append(note)
        elif isinstance(note, Timing):
            self._timings.append(note)

    def get_notes(self):
        self._notes.sort()
        return tuple(self._notes)

    def get_timings(self):
        self._timings.sort()
        return tuple(self._timings)

    def get_chart(self):
        self._chart = self._notes + self._timings
        self._chart.sort()
        return tuple(self._chart)

    def t2z(self, t):  # Transfer the Arcaea "x y t" unit to Minecraft "x y z" unit (static unit)
        z = 0
        bpm = 0
        for i in range(len(self._timings)):
            current_timing = self._timings[-i-1]  # Going through self._timings backward
            if current_timing.t1 <= t:  # If this timing is before the note (t)
                z += current_timing.bpm * (t - current_timing.t1)  # Distance between the note and the timing
                bpm = current_timing.bpm
                for n in range(len(self._timings)-i-1):  # For every timing before this one
                    z += self._timings[n].bpm * (self._timings[n+1].t1 - self._timings[n].t1)
                    # Add the complete distance before the note
                break
        #  z *= z_scale  # Calculate the distance in blocks
        return z, bpm

    def build(self, lane_width, y_scale, z_scale):
        # Prototype
        for note in self._notes:
            for block in note.get_blocks(lane_width, y_scale, z_scale * self.t2z(note.t1)[1]):
                x, y, z, (block, data) = block
                self.all_blocks.append({'x': x, 'y': y, 'z': z + z_scale * self.t2z(note.t1)[0], 'block': block, 'data': data})

    def __str__(self):
        return "Offset: {offset}, notes: {notes}".\
            format(
                offset=self.offset,
                notes=[str(n) for n in self._notes]
            )


