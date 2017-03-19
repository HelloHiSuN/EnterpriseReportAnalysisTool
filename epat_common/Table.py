# coding=utf-8


class Table(object):
    def __init__(self):
        self.row_num = 0
        self.current_line_max_col = 0
        self.sep_start_count = 0
        self.cells= []
        self.header = ''
        self.unit = ''
        self.section_info = ''

    def append(self, table_element):
        self.cells.append(table_element)

    def init_table_info(self, **kwargs):
        self.header = kwargs['header']
        self.unit = kwargs['unit']
        self.section_info = kwargs['section_info']
