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
    for cell in table.cells:
        if split_mode == SPLIT_COLUMN_2:
            # 表开始 或者 分割模式结束 新行开始
            if cell.y != y_old:
                while split_row_count < table.current_line_max_col:
                    row.append(u'')
                    split_row_count += 1
                split_row_count = 0
                split_mode = NO_SPLIT
                if row is not None:
                    res.append(row)
                table.row_num += 1
                table.current_line_max_col = 1
                table.sep_start_count = 0
                row = [cell.content]
                current_col_count = 1
                y_old = cell.y
                h_old = cell.h
            else:
                table.current_line_max_col += 1
                split_row_count += 1
                row.append(cell.content)

        elif split_mode == SPLIT_COLUMN_1:
            if cell.y == y_old and cell.h == h_old:
                table.current_line_max_col += 1
                current_col_count += 1
                row.append(cell.content)
            elif cell.y == y_old and cell.h != h_old:
                # 进入分割模式2
                split_mode = SPLIT_COLUMN_2
                res.append(row)
                current_col_count = 0
                table.row_num += 1
                row = []
                while append_none_count < table.sep_start_count:
                    row.append(u'')
                    append_none_count += 1
                    split_row_count += 1
                row.append(cell.content)
                split_row_count += 1
                table.current_line_max_col += 1
            elif cell.y == split_y_old and cell.h == split_h_old:
                current_col_count += 1
                row.append(cell.content)
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
                row.append(cell.content)
                current_col_count += 1

        elif cell.y != y_old and cell.h != h_old:
            # 进入分割模式1
            split_mode = SPLIT_COLUMN_1
            table.sep_start_count = table.current_line_max_col
            current_col_count += 1
            row.append(cell.content)
            split_y_old = cell.y
            split_h_old = cell.h

        else:
            table.current_line_max_col += 1
            current_col_count += 1
            row.append(cell.content)
    new_row = row[table.sep_start_count:]
    row = row[:table.sep_start_count]
    res.append(row)
    res.append(new_row)
    return res


if __name__ == "__main__":
    html = '<body><div class="c x9 yc0 w16 hb"><div class="t m0 x11 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">基本每股收益（元<span class="ff2 ls21">/</span>股）<span class="ff2 ws8"> </span></div></div><div class="c x2a yc0 w17 hb"><div class="t m0 x9 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">0.1 </div></div><div class="c x2c yc0 w19 hb"><div class="t m0 x1c h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">-0.15 </div></div><div class="c x31 yc0 w1b hb"><div class="t m0 x1c h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">-0.15 </div></div><div class="c x2e yc0 w19 hb"><div class="t m0 x21 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">166.67% </div></div><div class="c x27 yc0 w1c hb"><div class="t m0 x36 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">0.9 </div></div><div class="c x32 yc0 w1d hb"><div class="t m0 x37 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">0.43 </div></div><div class="c x9 yc1 w16 h9"><div class="t m0 x11 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">稀释每股收益（元<span class="ff2 ls21">/</span>股）<span class="ff2 ws8"> </span></div></div><div class="c x2a yc1 w17 h9"><div class="t m0 x9 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">0.1 </div></div><div class="c x2c yc1 w19 h9"><div class="t m0 x1c h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">-0.15 </div></div><div class="c x31 yc1 w1b h9"><div class="t m0 x1c h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">-0.15 </div></div><div class="c x2e yc1 w19 h9"><div class="t m0 x21 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">166.67% </div></div><div class="c x27 yc1 w1c h9"><div class="t m0 x36 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">0.9 </div></div><div class="c x32 yc1 w1d h9"><div class="t m0 x37 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">0.43 </div></div><div class="c x9 yc2 w16 h9"><div class="t m0 x11 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">加权平均净资产收益率<span class="ff2 ws8"> </span></div></div><div class="c x2a yc2 w17 h9"><div class="t m0 x2d h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">2.08% </div></div><div class="c x2c yc2 w19 h9"><div class="t m0 x23 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">-3.06% </div></div><div class="c x31 yc2 w1b h9"><div class="t m0 x23 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">-3.06% </div></div><div class="c x2e yc2 w19 h9"><div class="t m0 x38 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">5.14% </div></div><div class="c x27 yc2 w1c h9"><div class="t m0 x34 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">10.75% </div></div><div class="c x32 yc2 w1d h9"><div class="t m0 x34 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">10.39% </div></div><div class="c x9 yc3 w16 h16"><div class="t m0 x11 h3 yc4 ff2 fs0 fc0 sc0 ls2 ws8"> </div></div><div class="c x2a yc3 w17 h16"><div class="t m0 x30 h2 yc5 ff2 fs0 fc0 sc0 ls2 ws1">2014 <span class="ff1 ws2">年末</span><span class="ws8"> </span></div></div><div class="c x2c yc6 w18 ha"><div class="t m0 x39 h2 y2d ff2 fs0 fc0 sc0 ls2 ws1">2013 <span class="ff1 ws2">年末</span><span class="ws8"> </span></div></div><div class="c x2e yc6 w19 ha"><div class="t m0 x33 h2 y2e ff1 fs0 fc0 sc0 ls2">本年末比上年</div><div class="t m0 x30 h2 y8e ff1 fs0 fc0 sc0 ls2 ws2">末增减<span class="ff2 ws8"> </span></div></div><div class="c x27 yc6 w1a ha"><div class="t m0 x39 h2 y2d ff2 fs0 fc0 sc0 ls2 ws1">2012 <span class="ff1 ws2">年末</span><span class="ws8"> </span></div></div><div class="c x2c yc3 w19 h9"><div class="t m0 x30 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">调整前<span class="ff2 ws8"> </span></div></div><div class="c x31 yc3 w1b h9"><div class="t m0 x30 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">调整后<span class="ff2 ws8"> </span></div></div><div class="c x2e yc3 w19 h9"><div class="t m0 x30 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">调整后<span class="ff2 ws8"> </span></div></div><div class="c x27 yc3 w1c h9"><div class="t m0 x30 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">调整前<span class="ff2 ws8"> </span></div></div><div class="c x32 yc3 w1d h9"><div class="t m0 x30 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">调整后<span class="ff2 ws8"> </span></div></div><div class="c x9 yc7 w16 h9"><div class="t m0 x11 h2 y24 ff1 fs0 fc0 sc0 ls2 ws2">总资产（元）<span class="ff2 ws8"> </span></div></div><div class="c x2a yc7 w17 h9"><div class="t m0 x3a h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">1,005,009,097.67 </div></div><div class="c x2c yc7 w19 h9"><div class="t m0 x33 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">858,162,916.28 </div></div><div class="c x31 yc7 w1b h9"><div class="t m0 x33 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">858,162,916.28 </div></div><div class="c x2e yc7 w19 h9"><div class="t m0 x34 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">17.1<span class="_ _3"></span>1% </div></div><div class="c x27 yc7 w1c h9"><div class="t m0 x33 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">739,674,018.03 </div></div><div class="c x32 yc7 w1d h9"><div class="t m0 x33 h3 y7e ff2 fs0 fc0 sc0 ls2 ws8">756,196,092.23 </div></div><div class="c x9 yc8 w16 ha"><div class="t m0 x11 h2 y2e ff1 fs0 fc0 sc0 ls2">归属于上市公司股东的净</div><div class="t m0 x11 h2 y8e ff1 fs0 fc0 sc0 ls2 ws2">资产（元）<span class="ff2 ws8"> </span></div></div><div class="c x2a yc8 w17 ha"><div class="t m0 x1e h3 ya0 ff2 fs0 fc0 sc0 ls2 ws8">522,002,684.52 </div></div><div class="c x2c yc8 w19 ha"><div class="t m0 x33 h3 ya0 ff2 fs0 fc0 sc0 ls2 ws8">51<span class="_ _3"></span>1,276,765.15 </div></div><div class="c x31 yc8 w1b ha"><div class="t m0 x33 h3 ya0 ff2 fs0 fc0 sc0 ls2 ws8">51<span class="_ _3"></span>1,276,765.15 </div></div><div class="c x2e yc8 w19 ha"><div class="t m0 x38 h3 ya0 ff2 fs0 fc0 sc0 ls2 ws8">2.10% </div></div><div class="c x27 yc8 w1c ha"><div class="t m0 x33 h3 ya0 ff2 fs0 fc0 sc0 ls2 ws8">536,1<span class="_ _3"></span>14,223.81 </div></div><div class="c x32 yc8 w1d ha"><div class="t m0 x33 h3 ya0 ff2 fs0 fc0 sc0 ls2 ws8">547,343,675.75 </div></div></body>';
    from bs4 import BeautifulSoup
    from TableElement import TableElement
    from Table import Table
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    table = Table()

    for child in body:
        if is_table_tag(child):
            table_elem = TableElement(child)
            table.append(table_elem)

    res = parse_table(table)
    for row in res:
        for elem in row:
            print elem + ' || ',
        print


