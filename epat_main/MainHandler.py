# coding=utf-8

from bs4 import BeautifulSoup
from epat_common.TableParser import *
from epat_common.TagHandler import *
from epat_common.Table import Table
from epat_common.TableElement import TableElement
#########################
#
# 尝试解析 第三节 会计数据和财务重要指标摘要中的表格
#
# CREATE_DATE: 2017/02/19
# CREATE BY: Wenjie Sun
#
#########################


def get_ch3_start_page(page_content):
    for page in page_content:
        if isinstance(page, NavigableString):
            continue
        for div in page:
            if isinstance(div, NavigableString):
                continue
            count = 1
            for tag in div:
                if count != 4:
                    count += 1
                    continue
                if '第三节'.decode('utf8') in tag.get_text():
                    return page
                else:
                    break
            else:
                continue


def get_ch3_all_tables(ch3_start_tag):
    tag, end_flag = get_next_table_begin_tag(ch3_start_tag, "第四节")
    tables = []
    while not end_flag:
        res, last_tag = parse_table_base_5_col(tag)
        tables.append(res)
        last_tag = get_next_valid_tag(last_tag)
        tag, end_flag = get_next_table_begin_tag(last_tag, "第四节")
    return tables, tag


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


def get_ch3_tables(ch3_start_tag):
    tables = []
    tag, end_flag = get_next_table_begin_tag(ch3_start_tag, "第四节")
    while not end_flag:
        table = Table()
        table_element = TableElement(tag)
        table.append(table_element)
        while True:
            tag = get_next_valid_tag(tag)
            if is_table_tag(tag):
                table_element = TableElement(tag)
                table.append(table_element)
            else:
                tables.append(table)
                tag, end_flag = get_next_table_begin_tag(tag, "第四节")

                break
    return tables, tag


def main():
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test5/test5.html'), 'html.parser')
    page_content = get_page_content(soup)
    ch3_start_tag = get_ch3_start_tag(page_content)
    # tables, ch4_start_tag = get_ch3_all_tables(ch3_start_tag)
    tables, ch4_start_tag = get_ch3_tables(ch3_start_tag)

    tables_in_list = []
    for table in tables:
        table_in_list = parse_table(table)
        tables_in_list.append(table_in_list)

    for table in tables_in_list:
        print '================ table start ================'
        for row in table:
            for elem in row:
                print elem + '||',
            print
        print '================= table end ================='


if __name__ == '__main__':
    main()
