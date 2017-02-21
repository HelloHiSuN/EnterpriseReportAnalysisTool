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

CH3_TABLE_TYPE_1 = 1    # 会计数据和财务指标两个表合并
CH3_TABLE_TYPE_2 = 2    # 会计数据和财务指标两个表分离


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


# 返回表格头信息和表格开始div tag
# (table_info, table_start_tag)
def get_table_info(page):
    table_info = []
    tag = pass_page_info(page)
    target_div = tag.next_sibling   # 跳过章节信息
    # 到div的class出现c之前 都是表格头信息
    # 取出其中所有文本信息，一个div一行
    while "c" not in target_div.attrs["class"]:
        table_info.append(target_div.get_text())
        target_div = target_div.next_sibling
    return table_info, target_div


def get_ch3_type(table_info):
    regex = '公司是否因会计政策变更及会计差错更正等追溯调整或重述以前年度会计数据'.decode('utf-8')
    for info in table_info:
        if regex in info:
            return CH3_TABLE_TYPE_1
    return CH3_TABLE_TYPE_2


def parse_ch3_table_type2(table_start_tag):
    pass


def main():
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test5/test5.html'), 'html.parser')
    page_content = get_page_content(soup)
    target_page = get_ch3_start_page(page_content)
    (table_info, table_start_tag) = get_table_info(target_page)
    ch3_type = get_ch3_type(table_info)
    if ch3_type == CH3_TABLE_TYPE_1:
        res = parse_table_base_5_col(table_start_tag)
    else:
        parse_ch3_table_type2(table_start_tag)

    for line in table_info:
        print line
    for line in res:
        for elem in line:
            print elem + '||',
        print

if __name__ == '__main__':
    main()
