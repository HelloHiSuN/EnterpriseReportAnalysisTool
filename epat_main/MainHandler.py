# coding=utf-8

from bs4 import BeautifulSoup
from epat_common.TableParser import *
from epat_common.TagHandler import *
from epat_common.Table import Table
from epat_common.TableElement import TableElement
#########################
#
# 目前功能：按照一个通用的方法解析一整个文档的表格
# 问题：   有一些表格不适用，需要修改
#         单元格分割时使用latex样式显示
#
# CREATE_DATE: 2017/02/19
# CREATE BY: Wenjie Sun
#
#########################


def get_ch3_start_tag(page_content):
    tag = get_first_valid_tag(page_content)
    count = 0
    while True:
        if '第三节'.decode('utf8') in tag.get_text():
            if 0 == count:
                count += 1
                tag = get_next_valid_tag(tag)
            else:
                return tag
        else:
            tag = get_next_valid_tag(tag)


def get_ch_n_tables(ch_n_start_tag, end_text):
    tables = []
    res, end_flag = get_next_table_begin_tag(ch_n_start_tag, end_text)
    while not end_flag:
        params = {'unit':res['unit'], 'header':res['header'], 'section_info':res['section_info']}
        tag = res['tag']
        section_info = res['section_info']
        table = Table()
        table.init_table_info(**params)
        table_element = TableElement(tag)
        table.append(table_element)
        while True:
            tag = get_next_valid_tag(tag)
            try:
                if is_table_tag(tag):
                    table_element = TableElement(tag)
                    table.append(table_element)
                else:
                    tables.append(table)
                    res, end_flag = get_next_table_begin_tag(tag, end_text, section_info)
                    break
            except AttributeError:
                print 'a'
                print 'b'
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
    table_in_list = parse_table(table)
    print '******** table start ********'
    for info in table_info:
        print info
    for row in table_in_list:
        for elem in row:
            print elem + '||',
        print
    print '******** table end ********'


def main():
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test7/test7.html'), 'html.parser')
    page_content = get_page_content(soup)
    ch_start_tag = get_ch3_start_tag(page_content)

    end_flags = ['第三节', '第四节', '第五节', '第六节', '第七节', '第八节', '第九节', '第十节', '第十一节', '第十二节', '第十三节']
    for i in range(0, len(end_flags)):
        if 0 == i:
            continue
        tables, ch_start_tag = get_ch_n_tables(ch_start_tag, end_flags[i])
        print '=================== ', end_flags[i-1], ' Begin ========================'
        for table in tables:
            show_table(table)
        print '=================== ', end_flags[i - 1], ' End ========================'
        if ch_start_tag is None:
            break
    print '=================== ALL END ==================='


if __name__ == '__main__':
    main()
