from OOP_Prototype import *


def create_article(string):
    keyword = cut_string(string, "(", before=True)
    _ = cut_string(cut_string(string, "(", after=True), ")", before=True)
    attributes = _.split(",")
    print(attributes)
    if keyword == FloorTap.keyword:
        t, lane = attributes
        return FloorTap(t, lane)
    elif keyword == FloorHold.keyword:
        t1, t2, lane = attributes
        return FloorHold(t1, t2, lane)
    elif keyword == SkyNote.keyword:
        t1, t2, x1, x2, slidemethod, y1, y2, color, _, _ = attributes
        if attributes[-1] == 'true':
            pass
        else:
            pass


def cut_string(string, cut_at, after=False, before=False):
    index = string.find(cut_at)
    if after:
        return string[index+1:]
    elif before:
        return string[:index]
    else:
        return string


def main(filepath):
    f = open(filepath)
    raw = f.read()
    lines = raw.split("\n")
    print(lines)

    chart = Chart()
    working_str = lines.pop(0)
    chart.offset = int(cut_string(working_str, ":", after=True))
    lines.pop(0)  # "-" -- the separator

    for line in lines:
        chart.add_note(create_article(line))


if __name__ == '__main__':
    main("2.aff")
