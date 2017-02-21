# coding=utf-8

import os
import docker


DIR_NAME = "/Users/hellohi/pdf/"
DEST_DIR = "./output"
T_DEST_DIR = "./t_output"

class PDF2HTML(object):
    _dir_name = ""
    _filenames = []

    def __init__(self, path):
        self._dir_name = path

    def _get_file_names(self):
        self._filenames = os.listdir(self._dir_name);
        self._filenames = filter(lambda filename:filename.endswith(".pdf"), self._filenames)

    def _handle_one_file(self, filename):
        # 执行命令，将结果存放在临时目录 - 将html文件复制到目标目录 - 删除临时目录中的内容
        client = docker.from_env()
        client.containers.run('bwits/pdf2htmlex',
                              'pdf2htmlEX --embed-css 0 --embed-font 0 --embed-image 0 --embed-javascript 0 --embed-outline 0 --optimize-text 1 --dest-dir "' + DEST_DIR + '_' + filename[:-4] + '" ' + filename,
                              volumes={'/Users/hellohi/pdf':{'bind':'/pdf','mode':'rw'}},
                              remove=True)

    def do_convert_task(self):
        self._get_file_names()
        for filename in self._filenames:
            self._handle_one_file(filename)


if __name__ == "__main__":

    handler = PDF2HTML(DIR_NAME)
    handler.do_convert_task()
