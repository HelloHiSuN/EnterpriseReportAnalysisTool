# coding=utf-8

from TagHandler import *

#########################
#
# 表格解析方法
#
# CREATE_DATE: 2017/02/21
# CREATE BY: Wenjie Sun
#
#########################

BASE_5_COLUMN_COUNT = 5     # 表格列数基数为5
NO_SPLIT = 0                # 未进入拆分模式
SPLIT_COLUMN_1 = 1          # 拆分模式第一行
SPLIT_COLUMN_2 = 2          # 拆分模式第二行


#########################
#
# 解析列数基数为5的表格
# 支持列级拆分
# 跨页情况目前测试没问题
#
# CREATE_DATE: 2017/02/21
# CREATE BY: Wenjie Sun
#
#########################
def parse_table_base_5_col(cell_tag):
    res = []
    column_count = BASE_5_COLUMN_COUNT
    next_line_begin_at = 0
    split_mode = NO_SPLIT  # 是否进入拆分模式
    jump_page_mode = False

    # div class e.g. ['c','x9','yb5','w16','h14']
    # 通过第三个判断行
    # 一般是一行5个单元格
    # 如果有拆分则再计算
    current_class = None
    last_class = current_class
    line_count = -1
    count = 0
    while is_table_tag(cell_tag):
        if (count % column_count == 0) or ((split_mode == SPLIT_COLUMN_2) and (current_class != last_class)):
            # 新行开始
            line_count += 1
            count = 0
            last_class = current_class = cell_tag.attrs['class'][2]
            res.append([])

            # 如果是新的一页，第一行可能出问题，硬读取
            if jump_page_mode:
                while count < column_count:
                    if last_class != current_class:
                        res[line_count].append(u'')
                    else:
                        res[line_count].append(cell_tag.get_text())
                        cell_tag = cell_tag.next_sibling
                        last_class = current_class
                        current_class = cell_tag.attrs['class'][2]
                    count += 1
                jump_page_mode = False
                continue

            if split_mode == SPLIT_COLUMN_1:
                split_mode = SPLIT_COLUMN_2
                while count < next_line_begin_at:
                    res[line_count].append(u'')
                    count += 1

            elif split_mode == SPLIT_COLUMN_2:
                column_count = column_count - next_line_begin_at - 1
                next_line_begin_at = 0
                split_mode = NO_SPLIT

        if split_mode == SPLIT_COLUMN_2:
            column_count += 1

        if current_class != last_class:
            # 出现拆分
            column_count = BASE_5_COLUMN_COUNT
            split_mode = SPLIT_COLUMN_1
            next_line_begin_at = count

        res[line_count].append(cell_tag.get_text())
        if cell_tag.next_sibling is None:   # 当页结束，下一页可能还有
            cell_tag = get_next_valid_tag(cell_tag)
            jump_page_mode = True
        else:
            cell_tag = cell_tag.next_sibling
        last_class = current_class
        current_class = cell_tag.attrs['class'][2]
        count += 1

    return res, cell_tag.previous_sibling

