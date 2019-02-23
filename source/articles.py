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

notes: tuple of int, represeting time in ms

block: tuple (block, data)
    block: block instance from mcpi.block
    data: int, representing block's kind (s.a. saplings, wools, stained glass, etc.)

x y t AND x y z coordinates: Arcaea and Minecraft coordinates

"""


class Article(object):  # For "物件", renamed "article" because of collision with "object"
    keyword = None

    def __init__(self):
        self.start_time = None

    def check_class(self, other):  # Syntactic sugar
        assert isinstance(other, Article), "{} is not an instance of Article".format(other)

    def __gt__(self, other):
        self.check_class(other)
        return self.start_time > other.start_time

    def __ge__(self, other):
        self.check_class(other)
        return self.start_time >= other.start_time

    def __eq__(self, other):
        self.check_class(other)
        return self.start_time == other.start_time

    def __str__(self):
        return "Article instance at {time}ms.".format(time=self.start_time)


class Note(Article):
    def __init__(self):
        super().__init__()
        self.start_time, self.end_time,\
            self.start_lane, self.end_lane, \
            self.start_height, self.end_height = (None,) * 6
        self.block = (block.AIR, None)

    def get_blocks(self, x_scale, y_scale, z_scale):
        pass  # TODO: Not very sure what to do

    def __str__(self):
        return "{name} instance at {start_time}~{end_time}ms with pos x ({start_x}~{end_x}), y({start_y}~{end_y})".format(
            name=self.__class__.__name__,
            start_time=self.start_time, end_time=self.end_time,
            start_x=self.start_lane, end_x=self.end_lane,
            start_y=self.start_height, end_y=self.end_height)


class FloorNote(Note):
    def __init__(self, t1, t2, lane):
        super().__init__()
        self.start_lane, self.end_lane = (int(lane), int(lane))
        self.start_height, self.end_height = (0, 0)
        self.start_time, self.end_time = int(t1), int(t2)


class FloorTap(FloorNote):
    keyword = ""

    def __init__(self, t, lane):
        super().__init__(t, t, lane)
        self.block = block.STONE
        self.visual_length = 2  # visual width in blocks

    def get_blocks(self, lane_width, y_scale, z_scale):
        block_list = []
        for i in range(self.visual_length):
            for n in range(lane_width):
                #                  |---------------x--------------|   y  z            block
                block_list.append([self.start_lane*(lane_width+1)-n, -1, i].append(self.block))
        return block_list


class FloorHold(FloorNote):
    keyword = "hold"

    def __init__(self, t1, t2, lane):
        super().__init__(t1, t2, lane)
        self.block = 'blockForFloorHold'

    def get_blocks(self, lane_width, y_scale, z_scale):  # pls pass chart.z_scale*bpm as z_scale
        block_list = []
        for i in range(z_scale * (self.end_time - self.start_time)):
            for n in range(lane_width):
                #                  |---------------x--------------|   y  z            block
                block_list.append([self.start_lane*(lane_width+1)-n, -1, i].append(self.block))
        return block_list


class SkyNote(Note):
    keyword = "arc"

    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod):
        super().__init__()
        self.start_time, self.end_time = int(t1), int(t2)
        self.start_lane, self.end_lane = (int((float(x1)+0.5)*100)), (int((float(x2)+0.5)*100))
        self.start_height, self.end_height = (int(float(y1)*100)), (int(float(y2)*100))
        self.slidemethod = slidemethod

    def get_curve(self, lane_width, y_scale, z_scale): # return coords of the centre of the curve, z_scale is bpm*z_scale
        block_list=[]        
        t = 0
        x0, y0, z0, x1, y1, z1 = self.x1*lane_width*2, self.y1*y_scale, 0, self.x2*lane_width*2, self.y2*y_scale, (self.t2 - self.t1) * z_scale
        dx = x1 - x0
        dy = y1 - y0
        dz = int(z1)
        step = 1 / (dx + dy + dx)
        
        if self.slidemethod == 's':
            while(t<= 1):
                block = (x0+t*dx,y0+t*dy,z0+t+dz)
                block_list.append(block)
                t += step
        
        elif self.slidemethod == 'b':
            for i in range(dz+1):
                l = i / dz
                x = x0 + dx * -2 * l * l * (l - 1.5 )
                y = y0 + dy * -2 * l * l * (l - 1.5 )
                block = (x,y,z)
                block_list.append(block)


        elif self.slidemethod == 'si':
            return
        elif self.slidemethod == 'so':
            return
        elif self.slidemethod == 'sisi':
            return
        elif self.slidemethod == 'siso':
            return
        elif self.slidemethod == 'soso':
            return
        elif self.slidemethod == 'sosi':
            return
        return block_list        


class Arc(SkyNote):
    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod, color):
        super().__init__(t1, t2, x1, x2, y1, y2, slidemethod)
        self.color = int(color)
        self.block = ('magentaGlassBlock', 'lightBlueGlassBlock')

    def __str__(self):
        return "{name} instance at {start_time}~{end_time}ms with pos x ({start_x}~{end_x}), y({start_y}~{end_y})," \
               " slidemethod={slidemethod} and color={color}".format(
            name=self.__class__.__name__,
            start_time=self.start_time, end_time=self.end_time,
            start_x=self.start_lane, end_x=self.end_lane,
            start_y=self.start_height, end_y=self.end_height,
            slidemethod=self.slidemethod, color=self.color
        )


class SkyLine(SkyNote):
    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod, notes):
        super().__init__(t1, t2, x1, x2, y1, y2, slidemethod)
        self.notes = notes

    def __str__(self):
        return "{name} instance at {start_time}~{end_time}ms with pos x ({start_x}~{end_x}), y({start_y}~{end_y})," \
               " slidemethod={slidemethod}. Notes are: {notes}".format(
            name=self.__class__.__name__,
            start_time=self.start_time, end_time=self.end_time,
            start_x=self.start_lane, end_x=self.end_lane,
            start_y=self.start_height, end_y=self.end_height,
            slidemethod=self.slidemethod, notes=self.notes
        )


class Timing(Article):
    keyword = "timing"

    def __init__(self, time, bpm, beat):
        super().__init__()
        self.start_time = int(time)
        self.bpm = float(bpm)
        self.beat = float(beat)

    def __str__(self):
        return "Timing instance at {time}ms with bpm {bpm} and beat {beat}".format(time=self.start_time,
                                                                                   bpm=self.bpm,
                                                                                   beat=self.beat)


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
            if current_timing.start_time < t:  # If this timing is before the note (t)
                z += current_timing.bpm * (t - current_timing.start_time)  # Distance between the note and the timing
                bpm = current_timing.bpm
                for n in range(len(self._timings)-i-1):  # For every timing before this one
                    z += self._timings[n].bpm * (self._timings[n+1].start_time - self._timings[n].start_time)
                    # Add the complete distance before the note
                break
        z *= self.z_scale  # Calculate the distance in blocks
        return z, bpm

    def build(self):
        # Prototype
        for note in self._notes:
            for block in note.get_blocks():
                x, y, z, (block, data) = block
                self.all_blocks.append({'x': x, 'y': y, 'z': z, 'block': block, 'data': data})

    def __str__(self):
        return "Offset: {offset}, notes: {notes}".format(offset=self.offset, notes=[str(n) for n in self._notes])


