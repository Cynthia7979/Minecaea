import articles


def create_article(string):
    if string in ("", " ", "\n") or string.startswith("#"):
        return None
    keyword = cut_string(string, "(", before=True)
    all_attributes = cut_string(cut_string(string, "(", after=True), ")", before=True)
    attributes = all_attributes.split(",")
    if keyword == articles.FloorTap.keyword:
        t, lane = attributes
        return articles.FloorTap(t, lane)
    elif keyword == articles.FloorHold.keyword:
        t1, t2, lane = attributes
        return articles.FloorHold(t1, t2, lane)
    elif keyword == articles.SkyNote.keyword:
        t1, t2, x1, x2, slidemethod, y1, y2, color, _, skyline_boolean = attributes
        if skyline_boolean == 'true':
            all_notes = cut_string(cut_string(string, "[", after=True), "]", before=True)
            notes = []
            for note in all_notes.split(','):
                notes.append(cut_string(cut_string(note, "(", after=True), ")", before=True))
            return articles.SkyLine(t1, t2, x1, x2, y1, y2, slidemethod, notes)
        else:
            return articles.Arc(t1, t2, x1, x2, y1, y2, slidemethod, color)
    elif keyword == articles.Timing.keyword:
        time, bpm, beat = attributes
        return articles.Timing(time, bpm, beat)


def cut_string(string, cut_at, after=False, before=False):
    index = string.find(cut_at)
    if index == -1:
        return ""
    if after:
        return string[index+1:]
    elif before:
        return string[:index]
    else:
        return string


def load(filepath):
    f = open(filepath)
    raw = f.read()
    lines = raw.split("\n")

    chart = articles.Chart()
    working_str = lines.pop(0)
    chart.offset = int(cut_string(working_str, ":", after=True))
    lines.pop(0)  # "-" -- the separator

    for line in lines:
        chart.add_note(create_article(line))
    return chart


if __name__ == '__main__':
    load("test.aff")
