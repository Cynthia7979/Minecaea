# -*- coding: gb2312 -*-

"""
Minecaea - Minecraft version of Arcaea
class structure prototype
============================

x-axis: int
    leftmost = 0
    rightmost = 200
    center = 100

y-axis: int
    uppermost = 100 (sky tap line)
    bottommost = 0 (floor)
    center = 50

lane: int
    leftmost = 1
    rightmost = 4

color: int
    0 = blue
    1 = red

notes: tuple of int, represeting time in ms

x_init, y_init: int
    * bottomleft and upperleft of the actual playing area in the map, z = 0 (on ground)
"""


class Article(object):  # For "���", renamed "article" because of collision with "object"
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
        self.block = 'airBlock'

    def place_block(self, x_scale, y_scale, z_scale):
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
        self.block = (1,none)
        self.visual_length = 2 #unit in blocks

    def place_block(self, lane_width, y_scale, z_scale):
        block_list = []
        for i in range(self.visual_length):
            for n in range(lane_width):
                bolck_list.append([self.lane*(lane_width+1)-n, -1, i].append(self.block))
        return block_list


class FloorHold(FloorNote):
    keyword = "hold"

    def __init__(self, t1, t2, lane):
        super().__init__(t1, t2, lane)
        self.block = 'blockForFloorHold'

    def place_block(self, lane_width, y_scale, z_scale): #pls pass chart.z_scale*bpm as z_scale
        for i in range(z_scale * (self.end_time - self.start_time)):
            for n in range(lane_width):
                bolck_list.append([self.lane*(lane_width+1)-n, -1, i].append(self.block))
        return block_list


class SkyNote(Note):
    keyword = "arc"

    def __init__(self, t1, t2, x1, x2, y1, y2, slidemethod):
        super().__init__()
        self.start_time, self.end_time = int(t1), int(t2)
        self.start_lane, self.end_lane = (int((float(x1)+0.5)*100)), (int((float(x2)+0.5)*100))
        self.start_height, self.end_height = (int(float(y1)*100)), (int(float(y2)*100))
        self.slidemethod = slidemethod


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
        self.z_scale = 1

    def add_note(self, note):
        if isinstance(note, Note):  # If it isn't a blank line, comment or something
            self._notes.append(note)
        elif isinstance(note,Timing):
            self._timings.append(note)

    def get_chart(self):
        self._notes.sort()
        return tuple(self._notes)

    def get_timings(self):
        self._timings.sort()
        return tuple(self._timings)

    def t2z(self,t):
        z = 0
        bpm = 0
        for i in range(len(self._timings)):
            if self._timings[-i-1].start_time < t:
                z = z + self._timings[-i-1].bpm * ( t - self._timings[-i-1].start_time )
                bpm = self._timings[-i-1].bpm
                for n in range(len(self._timings)-i-1):
                    z = z + self._timings[n].bpm * ( self._timings[n+1].start_time - self._timings[n].start_time )
                break
        z *= self.z_scale
        return z, bpm

    def __str__(self):
        return "Offset: {offset}, notes: {notes}".format(offset=self.offset, notes=[str(n) for n in self._notes])


