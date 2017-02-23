# coding=utf-8

from bs4 import BeautifulSoup
from pprint import pprint
from epat_common.TableParser import *
from epat_common.TagHandler import *

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


def get_ch3_all_tables(start_page_tag):
    table_begin_tag = get_table_begin_tag_in_page(start_page_tag)
    tables = []
    res, last_tag = parse_table_base_5_col(table_begin_tag)
    tables.append(res)
    still_in_ch3 = True
    while still_in_ch3:
        last_tag = get_next_valid_tag(last_tag)
        while not is_table_tag(last_tag):
            text = last_tag.get_text()
            if '董事会报告'.decode('utf8') in text:  # 到达第四节 董事会报告
                still_in_ch3 = False
                break
            last_tag = get_next_valid_tag(last_tag)
        if still_in_ch3:
            res, last_tag = parse_table_base_5_col(last_tag)
            tables.append(res)
    return tables, last_tag


def main():
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test2/test2.html'), 'html.parser')
    page_content = get_page_content(soup)
    ch3_start_page = get_ch3_start_page(page_content)
    tables, last_tag = get_ch3_all_tables(ch3_start_page)
    for table in tables:
        print '================ table start ================'
        for row in table:
            for elem in row:
                print elem + '||',
            print
        print '================= table end ================='


if __name__ == '__main__':
    main()
