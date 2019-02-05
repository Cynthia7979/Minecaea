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


class Note(object):
    def __init__(self):
        self.start_time, self.end_time,\
            self.start_lane, self.end_lane, \
            self.start_height, self.end_height = (None,) * 6
        self.block = airBlock

    def place_block(self, x_init, y_init, t):
        pass  # TODO: Not very sure what to do because of time

    def check_class(self, other):  # Syntactic sugar
        assert isinstance(other, Note), "{} is not an instance of Note".format(other)

    def __gt__(self, other):
        self.check_class(other)
        return self.start_time > other.start_time

    def __ge__(self, other):
        self.check_class(other)
        return self.start_time >= other.start_time

    def __eq__(self, other):
        self.check_class(other)
        return self.start_time == other.start_time


class FloorNote(Note):
    def __init__(self, lane):
        super().__init__()
        self.start_lane, self.end_lane = (lane, lane)
        self.start_height, self.end_height = (0, 0)


class FloorTap(FloorNote):
    def __init__(self, t, lane):
        super().__init__(lane)
        self.start_time, self.end_time = t, t
        self.block = blockForFloorTap


class FloorHold(FloorNote):
    def __init__(self, t1, t2, lane):
        super().__init__(lane)
        self.start_time, self.end_time = t1, t2
        self.block = blockForFloorHold


class SkyNote(Note):
    def __init__(self, t1, t2, x1, x2, y1, y2):
        super().__init__()
        self.start_time, self.end_time = t1, t2
        self.start_lane, self.end_lane = x1, x2
        self.start_height, self.end_height = y1, y2


class Arc(SkyNote):
    def __init__(self, t1, t2, x1, x2, y1, y2, color):
        super().__init__(t1, t2, x1, x2, y1, y2)
        self.color = color
        self.block = (magentaGlassBlock, lightBlueGlassBlock)


class SkyLine(SkyNote):
    def __init__(self, t1, t2, x1, x2, y1, y2, notes):
        super().__init__(t1, t2, x1, x2, y1, y2)
        self.notes = notes

