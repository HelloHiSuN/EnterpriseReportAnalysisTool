# coding=utf-8

import os
import docker


DIR_NAME = "/Users/hellohi/pdf/source"
DEST_DIR = "./html_output"


class PDF2HTML(object):
    _dir_name = ""
    _filenames = []

    def __init__(self, path):
        self._dir_name = path

    def _get_file_names(self):
        self._filenames = os.listdir(self._dir_name)
        self._filenames = filter(lambda filename: filename.endswith(".pdf"), self._filenames)

    @staticmethod
    def handle_one_file(filename):
        client = docker.from_env()
        client.containers.run('bwits/pdf2htmlex-alpine',
                              'pdf2htmlEX --dest-dir "' + DEST_DIR + '" ' + filename,
                              volumes={DIR_NAME: {'bind': '/pdf', 'mode': 'rw'}},
                              remove=True)

    def do_convert_task(self):
        self._get_file_names()
        for filename in self._filenames:
            print 'Handle ', filename, '...'
            try:
                self.handle_one_file(filename)
            except Exception, e:
                print '********[ERROR] ', filename, ' Wrong!********'
                print e.message
                continue
            print filename, ' Done!'


if __name__ == "__main__":
    handler = PDF2HTML(DIR_NAME)
    handler.do_convert_task()
