# coding=utf-8


class TableElement(object):
    def __init__(self, tag):

        self.x = tag.attrs['class'][1]
        self.y = tag.attrs['class'][2]
        self.w = tag.attrs['class'][3]
        self.h = tag.attrs['class'][4]
        self.content = tag.get_text()

