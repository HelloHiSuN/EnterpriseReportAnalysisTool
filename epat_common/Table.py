# coding=utf-8


class Table(object):
    def __init__(self):
        self.row_num = 0
        self.current_line_max_col = 0
        self.sep_start_count = 0
        self.cells= []

    def append(self, table_element):
        self.cells.append(table_element)
