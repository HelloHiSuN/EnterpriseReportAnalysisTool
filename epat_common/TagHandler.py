# coding=utf-8

from bs4.element import NavigableString
import re

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
            elif is_table_tag(target_div):
                return target_div
            elif target_div.get_text().strip():
                return target_div
    page_tag = get_next_page_tag(page_tag)
    if page_tag is None:
        return None
    return pass_page_info(page_tag)


# 获取start_tag之后,遇到结束文本之前表格开始的tag
def get_next_table_begin_tag(tag, end_text, section_info=None):
    ch_pattern = re.compile(u'^.*[一二三四五六七八九十]{1,2}、.*$')
    section_pattern = re.compile(u'^.*[0-9]{1,2}、.*$')
    unit_pattern = re.compile(u'^.*单位.*$')
    rb_pattern = re.compile(u'^.*□.*$')
    res = {}
    old_tag_1 = None
    old_tag_2 = None
    while not is_table_tag(tag):
        if old_tag_1 is None:
            old_tag_1 = tag
        else:
            old_tag_2 = old_tag_1
            old_tag_1 = tag
        if end_text.decode('utf8') in tag.get_text():
            res['tag'] = tag
            res['header'] = None
            return res, True
        tag_content = tag.get_text()
        if ch_pattern.match(tag_content) or section_pattern.match(tag_content):
            section_info = tag_content
        tag = get_next_valid_tag(tag)
        if tag is None:
            res['tag'] = None
            return res, True
    if old_tag_1 is None:
        res['header'] = False
    elif unit_pattern.match(old_tag_1.get_text()):
        res['unit'] = old_tag_1.get_text()
        if old_tag_2 is not None:
            if rb_pattern.match(old_tag_2.get_text()):
                res['header'] = False
            else:
                res['header'] = old_tag_2.get_text()
        else:
            res['header'] = False
    elif rb_pattern.match(old_tag_1.get_text()):
        res['unit'] = False
        if old_tag_2 is not None:
            res['header'] = old_tag_2.get_text()
        else:
            res['header'] = False
    else:
        res['unit'] = False
        res['header'] = old_tag_1.get_text()
    res['section_info'] = section_info
    res['tag'] = tag
    return res, False


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
