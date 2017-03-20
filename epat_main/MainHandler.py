# coding=utf-8

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
            tag = get_next_valid_tag(tag)
            if is_table_tag(tag):
                table_element = TableElement(tag)
                table.append(table_element)
            else:
                tables.append(table)
                res, end_flag = get_next_table_begin_tag(tag, end_text, section_info)
                break
    tag = res['tag']
    return tables, tag


def show_table(table):
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
        print '******** table start ********'
        for info in table_info:
            print info
        for row in table_in_list:
            for elem in row:
                print elem,
                print ' || ',
            print
        print '******** table end ********'
    except IndexError:
        print '######## TABLE ERROR ########'
        for info in table_info:
            print info
        print '######## TABLE ERROR ########'


def main():
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test2/test2.html'), 'html.parser')
    # soup = BeautifulSoup(open('/Users/hellohi/pdf/test2.html'), 'html.parser')
    page_content = get_page_content(soup)

    start_tag = get_first_valid_tag(page_content)
    tables, tag = get_tables(start_tag, 'NEVER_APPEAR_IN_DOC_STR')
    for table in tables:
        show_table(table)


if __name__ == '__main__':
    main()
