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
    return get_parent_page_tag(tag).next_sibling


# 跳过页面的<img><页眉><页脚>
def pass_page_info(page_tag):
    for tag in page_tag.children:
        # 跳过一个<img /> 页眉div 页脚div
        count = 0
        for target_div in tag:
            if count < 3:
                count += 1
            else:
                return target_div

