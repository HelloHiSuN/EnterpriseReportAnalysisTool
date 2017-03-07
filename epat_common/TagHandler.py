# coding=utf-8

from bs4.element import NavigableString

#########################
#
# 用于对 HTML Tag 进行相关操作
#
# CREATE_DATE: 2017/02/21
# CREATE BY: Wenjie Sun
#
#########################


# 获得整体HTML的page_content
def get_page_content(soup):
    body = soup.body
    for child in body.children:
        if isinstance(child, NavigableString):
            continue
        if child.attrs['id'] == 'page-container':
            return child


# 获得tag的页面级父节点
def get_parent_page_tag(tag):
    while 'data-page-no' not in tag.attrs:
        tag = tag.parent
    return tag


# 获得下一页的页面级tag
def get_next_page_tag(tag):
    tag = get_parent_page_tag(tag)
    for sibling in tag.next_siblings:
        if isinstance(sibling, NavigableString):
            continue
        return sibling
    return None


# 跳过页面的<img><页眉><页脚>
def pass_page_info(page_tag):

    for tag in page_tag.children:
        # 跳过一个<img /> 页眉div 页脚div
        count = 0
        for target_div in tag:
            if count < 3:
                count += 1
            elif target_div.get_text().strip():
                return target_div


# 获取start_tag之后,遇到结束文本之前表格开始的tag
def get_next_table_begin_tag(tag, end_text):
    while not is_table_tag(tag):
        if end_text.decode('utf8') in tag.get_text():
            return tag, True
        tag = get_next_valid_tag(tag)
        if tag is None:
            return None, True
    return tag, False


# 判断tag是不是表格tag
def is_table_tag(tag):
    return 'c' in tag.attrs['class']


# 获取整个文档第一个有效tag
def get_first_valid_tag(page_content):
    for tag in page_content:
        if isinstance(tag, NavigableString):
            continue
        return pass_page_info(tag)


# 获取下一个有效tag
def get_next_valid_tag(tag):
    if tag.next_sibling is None:
        tag = get_next_page_tag(tag)
        if tag is None:
            return None
        tag = pass_page_info(tag)
    else:
        tag = tag.next_sibling
    return tag
