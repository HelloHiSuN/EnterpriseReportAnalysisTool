# coding=utf-8

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from pprint import pprint

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
COMMON_COLUMN_COUNT = 5   # 一般性一行单元格数量
NO_SPLIT = 0
SPLIT_COLUMN_1 = 1
SPLIT_COLUMN_2 = 2


def get_page_content(body):
    for child in body.children:
        if isinstance(child, NavigableString):
            continue
        if child.attrs['id'] == 'page-container':
            return child


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
    for tag in page.children:
        # 只需要第一个<div>

        # 跳过一个<img /> 页眉div 页脚div 章节信息
        count = 0
        for target_div in tag:
            if count < 4:
                count +=1
                continue
            # 到div的class出现c之前 都是表格头信息
            # 取出其中所有文本信息，一个div一行
            if "c" in target_div.attrs["class"]:
                return table_info, target_div
            table_info.append(target_div.get_text())


def get_ch3_type(table_info):
    regex = '公司是否因会计政策变更及会计差错更正等追溯调整或重述以前年度会计数据'.decode('utf-8')
    for info in table_info:
        if regex in info:
            return CH3_TABLE_TYPE_1
    return CH3_TABLE_TYPE_2


def parse_ch3_table_type1(cell_tag):
    res = []
    column_count = COMMON_COLUMN_COUNT
    next_line_begin_at = 0
    split_mode = NO_SPLIT  # 是否进入拆分模式

    # div class e.g. ['c','x9','yb5','w16','h14']
    # 通过第三个判断行
    # 一般是一行5个单元格
    # 如果有拆分则再计算

    current_class = None
    last_class = current_class
    line_count = -1
    count = 0
    while 'c' in cell_tag.attrs['class']:
        if (count % column_count == 0) or ((split_mode == SPLIT_COLUMN_2) and (current_class != last_class)):
            # 新行开始
            line_count += 1
            count = 0
            last_class = current_class = cell_tag.attrs['class'][2]
            res.append([])
            if split_mode == SPLIT_COLUMN_1:
                split_mode = SPLIT_COLUMN_2
                while count < next_line_begin_at:
                    res[line_count].append(' ')
                    count += 1

            elif split_mode == SPLIT_COLUMN_2:
                column_count = column_count - next_line_begin_at - 1
                next_line_begin_at = 0
                split_mode = NO_SPLIT

        if split_mode == SPLIT_COLUMN_2:
            column_count += 1

        if current_class != last_class:
            # 出现拆分
            column_count = COMMON_COLUMN_COUNT
            split_mode = SPLIT_COLUMN_1
            next_line_begin_at = count

        res[line_count].append(cell_tag.get_text())
        cell_tag = cell_tag.next_sibling
        last_class = current_class
        current_class = cell_tag.attrs['class'][2]
        count += 1

    return res


def parse_ch3_table_type2(table_start_tag):
    pass


def main():
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test5/test5.html'), 'html.parser')
    body = soup.body
    page_content = get_page_content(body)
    target_page = get_ch3_start_page(page_content)
    (table_info, table_start_tag) = get_table_info(target_page)
    ch3_type = get_ch3_type(table_info)
    if ch3_type == CH3_TABLE_TYPE_1:
        res = parse_ch3_table_type1(table_start_tag)
    else:
        parse_ch3_table_type2(table_start_tag)
    for line in res:
        for ele in line:
            print ele + '||',
        print

if __name__ == '__main__':
    main()
