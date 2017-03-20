# coding=utf-8

from TagHandler import *
from TableElement import TableElement
#########################
#
# 表格解析方法
#
# CREATE_DATE: 2017/02/21
# CREATE BY: Wenjie Sun
#
#########################

NO_SPLIT = 0                # 未进入拆分模式
SPLIT_COLUMN_1 = 1          # 拆分模式第一行
SPLIT_COLUMN_2 = 2          # 拆分模式第二行


def parse_table(table):
    res = []
    row = None
    y_old = "something"
    h_old = "something"
    split_y_old = "something"
    split_h_old = "something"
    split_mode = SPLIT_COLUMN_2
    append_none_count = 0
    split_row_count = 0
    current_col_count = 0
    last_row = None
    last_sep_cell = []
    for cell in table.cells:
        if split_mode == SPLIT_COLUMN_2:
            # 表开始 或者 分割模式结束 新行开始
            if cell.y != y_old:
                while split_row_count < table.current_line_max_col:
                    row.append(TableElement())
                    split_row_count += 1
                split_row_count = 0
                split_mode = NO_SPLIT
                if last_row is not None:
                    if last_sep_cell[1] != 1:
                        last_row[last_sep_cell[0]].content = '[' + str(last_sep_cell[1]) + '] ' + last_row[last_sep_cell[0]].content
                    res.append(last_row)
                    last_row = None
                if row is not None:
                    res.append(row)
                table.row_num += 1
                table.current_line_max_col = 1
                table.sep_start_count = 0
                row = [cell]
                current_col_count = 1
                y_old = cell.y
                h_old = cell.h
            else:
                for i in range(len(last_row)):
                    if last_row[i].x == cell.x:
                        if last_sep_cell[1] != 1:
                            last_row[last_sep_cell[0]].content = '[' + str(last_sep_cell[1]) + '] ' + last_row[last_sep_cell[0]].content
                        last_sep_cell = [i, 0]
                        break
                last_sep_cell[1] += 1
                table.current_line_max_col += 1
                split_row_count += 1
                row.append(cell)

        elif split_mode == SPLIT_COLUMN_1:
            if cell.y == y_old and cell.h == h_old:
                table.current_line_max_col += 1
                current_col_count += 1
                row.append(cell)
            elif cell.y == y_old and cell.h != h_old:
                # 进入分割模式2
                split_mode = SPLIT_COLUMN_2
                last_row = row
                # res.append(row)             # 记录这一行，在做分割标记处理后添加到结果集
                current_col_count = 0
                table.row_num += 1
                row = []
                while append_none_count < table.sep_start_count:
                    row.append(TableElement())
                    append_none_count += 1
                    split_row_count += 1
                for i in range(0,len(last_row)):
                    if last_row[i].x == cell.x:
                        last_sep_cell = [i, 1]
                        break
                row.append(cell)
                split_row_count += 1
                table.current_line_max_col += 1
            elif cell.y == split_y_old and cell.h == split_h_old:
                current_col_count += 1
                row.append(cell)
            else:
                # 重置分割模式
                new_row = row[table.sep_start_count:]
                row = row[:table.sep_start_count]
                res.append(row)

                row = new_row
                table.current_line_max_col = current_col_count - table.current_line_max_col
                # table.current_line_max_col -= table.sep_start_count
                table.sep_start_count = table.current_line_max_col
                current_col_count = table.current_line_max_col
                table.row_num += 2
                y_old = split_y_old
                h_old = split_h_old
                split_y_old = cell.y
                split_h_old = cell.h
                row.append(cell)
                current_col_count += 1

        # elif cell.y != y_old and cell.h != h_old:
        elif cell.y != y_old:
            # 进入分割模式1
            split_mode = SPLIT_COLUMN_1
            table.sep_start_count = table.current_line_max_col
            current_col_count += 1
            row.append(cell)
            split_y_old = cell.y
            split_h_old = cell.h

        else:
            table.current_line_max_col += 1
            current_col_count += 1
            row.append(cell)
    new_row = row[table.sep_start_count:]
    row = row[:table.sep_start_count]
    res.append(row)
    res.append(new_row)
    return res
