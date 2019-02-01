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

slidemethod: list of int
    * Not very clear what this meant
    0 = both (b, sine in + out)
    1 = straight (s)
    2 = sine in (si)
    3 = sine out (so)
    * [] for skytap

color: int
    0 = blue
    1 = red
"""

class Note(object):
    def __init__(self):
        self.start_time, self.end_time,\
        self.start_lane, self.end_lane, \
        self.start_height, self.end_height = (None,) * 6
        self.block = None


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
    def __init__(self, t1, t2, x1, x2, slidemethod, y1, y2, color):
        super().__init__(t1, t2, x1, x2, y1, y2)
        self.slidemethod = slidemethod
        self.color = color
        self.block = bloc
