# coding=utf-8
from bs4 import BeautifulSoup
from bs4.element import NavigableString

#########################
#
# 尝试解析 第三节 会计数据和财务重要指标摘要中的表格
#
# CREATE_DATE: 2017/02/19
# CREATE BY: Wenjie Sun
#
#########################



def get_page_content(body):
    for child in body.children:
        if isinstance(child, NavigableString):
            continue
        if child.attrs['id'] == 'page-container':
            return child

#迭代有问题 待修改
def get_ch3_start_page(page_content):
    for page in page_content:
        if isinstance(page, NavigableString):
            continue
        for div in page:
            if isinstance(div, NavigableString):
                continue
            if 'opened' in div.attrs['class']:
                count = 1
                for tag in div:
                    if count != 4:
                        count += 1
                        continue
                    if '第三节' in tag.get_text():
                        return page
                    else:
                        break
            else:
                continue


if __name__ == '__main__':
    soup = BeautifulSoup(open('/Users/hellohi/pdf/output_test2/test2.html'), 'html.parser')
    body = soup.body
    page_content = get_page_content(body)
    target_page = get_ch3_start_page(page_content)
    print target_page
    # for child in page_content:
    #     if isinstance(child, NavigableString):
    #         continue
    #     print '==========='
    #     print child
    #     print '==========='
