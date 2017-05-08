#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import csv
from io import StringIO
import codecs
import random


class CsvFile:
    def __init__(self):
        pass

    def cur_file_dir(self):
        # 获取脚本路径
        path = sys.path[0]
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    _csv_file = None
    _writer = None
    _Reader = None

    def open(self, filePath):
        path = self.cur_file_dir() + '/' + filePath
        #self._csv_file = open(path, 'w+', newline='', encoding='utf-8')
        self._csv_file = codecs.open(path, 'w', 'utf_8_sig')
        self._writer = csv.writer(self._csv_file)

    def close(self):
        self._csv_file.close()

    def writerow(self, content):
        self._writer.writerow(content)

# test


def test():
    csv_file = CsvFile()
    csv_file.open('test.csv')
    csv_file.writerow(('一二三', 'abc'))
    rows = []
    ###
    row = ['@1', '@2', '@3']
    rows.append(row)
    row = ['#1', '#2', '#3']
    rows.append(row)
    row = ['!1', '!2', '!3']
    rows.append(row)
    ###
    rows.append(['!1', '!2', '!3'])
    rows.append(['#1', '#2', '#3'])
    rows.append(['@1', '@2', '@3'])
    rows.append('123')
    rows.append('abc')
    for row in rows:
        csv_file.writerow(row)
    csv_file.close()


# test()
