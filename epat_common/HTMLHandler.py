# coding=utf-8

import codecs
from bs4 import BeautifulSoup
from epat_common.TableParser import *
from epat_common.TagHandler import *
from epat_common.Table import Table
from epat_common.TableElement import TableElement
#########################
#
# 目前功能： 按照一个通用的方法解析一整个文档的表格
#           单元格分割时使用latex样式显示
# 问题：     有一些表格不适用，不适用是报错
#           收入 行业分类 类型表格处理不正确
#
# CREATE_DATE: 2017/02/19
# CREATE BY: Wenjie Sun
#
#########################


class HTMLHandler(object):
    def __init__(self, html_path, output_path):
        self.soup = BeautifulSoup(open(html_path), 'html.parser')
        self.page_content = get_page_content(self.soup)
        self.output_path = output_path

    @staticmethod
    def get_tables(start_tag, end_text):
        tables = []
        res, end_flag = get_next_table_begin_tag(start_tag, end_text)
        while not end_flag:
            params = {'unit': res['unit'], 'header': res['header'], 'section_info': res['section_info']}
            tag = res['tag']
            section_info = res['section_info']
            table = Table()
            table.init_table_info(**params)
            table_element = TableElement(tag)
            table.append(table_element)
            while True:
                try:
                    tag = get_next_valid_tag(tag)
                    if is_table_tag(tag):
                        table_element = TableElement(tag)
                        table.append(table_element)
                    else:
                        tables.append(table)
                        res, end_flag = get_next_table_begin_tag(tag, end_text, section_info)
                        break
                except Exception, e:
                    raise e
        tag = res['tag']
        return tables, tag

    @staticmethod
    def show_table(table, output, table_count):
        table_info = []
        if table.section_info is not None:
            table_info = [table.section_info]
        if table.header:
            if table.section_info is None or table.header not in table.section_info :
                table_info.append(table.header)
        if table.unit:
            table_info.append(table.unit)
        try:
            table_in_list = parse_table(table)
            msg = '******** table start ********'
            output.write(msg + '\n')
            for info in table_info:
                msg = info
                output.write(msg + '\n')
            for row in table_in_list:
                for elem in row:
                    output.write(str(elem).decode('utf-8'))
                    output.write(' || ')
                output.write('\n')
            msg = '******** table end ********'
            output.write(msg + '\n')
            table_count[0] += 1
        except IndexError:
            msg = '######## TABLE ERROR ########'
            output.write(msg + '\n')
            for info in table_info:
                msg = info
                output.write(msg + '\n')
            msg = '######## TABLE ERROR ########'
            output.write(msg + '\n')
            table_count[1] += 1

    def do_extract_task(self):
        start_tag = get_first_valid_tag(self.page_content)
        try:
            tables, tag = self.get_tables(start_tag, 'NEVER_APPEAR_IN_DOC_STR')
        except Exception, e:
            raise e
        output = codecs.open(self.output_path, 'w', 'utf-8')
        table_count = [0, 0]
        for table in tables:
            self.show_table(table, output, table_count)
        output.write('----------------------------\n')
        total = 'Total: ' + str((table_count[0] + table_count[1])) + '\n'
        output.write(total)
        success = 'Success: ' + str(table_count[0]) + '\n'
        output.write(success)
        error = 'Error: ' + str(table_count[1]) + '\n'
        output.write(error)
        accuracy = 'Accuracy:' + str(1.0*table_count[0]/(table_count[0]+table_count[1])) + '%\n'
        output.write(accuracy)
        output.close()
