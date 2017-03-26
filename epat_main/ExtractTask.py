# coding=utf-8

import os
from epat_common.HTMLHandler import HTMLHandler
#########################
#
# 控制读取所有html文档，解析其中的表格
# 每个文档的结果存放在一个txt中
#
# CREATE_DATE: 2017/02/19
# CREATE BY: Wenjie Sun
#
#########################

OUTPUT_DIR = '/Users/hellohi/pdf/txt_output'
INPUT_DIR = '/Users/hellohi/pdf/html_output'


def txt_path_gen(html_file_path):
    filename = html_file_path.split('/')[-1].split('.')[0] + '.txt'
    return OUTPUT_DIR + '/' + filename

if __name__ == '__main__':
    # html_handler = HTMLHandler('/Users/hellohi/pdf/test.html','/Users/hellohi/pdf/test.txt')
    # html_handler.do_extract_task()
    html_list = os.listdir(INPUT_DIR)
    html_list = filter(lambda filename: filename.endswith(".html"), html_list)
    for html_filename in html_list:
        input_path = html_filename if INPUT_DIR in html_filename else INPUT_DIR + '/' + html_filename
        output_path = txt_path_gen(input_path)
        print '[INFO] Extract File:', html_filename, ' Now...'
        try:
            html_handler = HTMLHandler(input_path, output_path)
            html_handler.do_extract_task()
            print '[INFO] Extract File:', html_filename, ' Done!'
        except Exception, e:
            print e.message
            print '********[ERROR] Extract File:', html_filename, ' Wrong!********'

    # html_handler = HTMLHandler(input_path, output_path)
    # html_handler.do_extract_task()

