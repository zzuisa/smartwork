# -*- encoding: utf-8 -*-
'''
@文件        :encoding_converter_tools.py
@说明        :
@时间        :2022/10/18 10:16:37
@作者        :awx1192780
@版本        :1.0
'''

import codecs
import os
import sys
import shutil
import re
import chardet
from util.common_tools import print_pro
from base import constants
convertfiletypes = [
    ".xml",
    ".lua",
    ".csd",
    ".py",
    ".txt"
]


def check_need_convert(filename):
    for filetype in convertfiletypes:
        if filename.lower().endswith(filetype):
            return True
    return False


total_cnt = 0
success_cnt = 0
unkown_cnt = 0


def convert_encoding_to_utf_8(filename):
    global total_cnt, success_cnt, unkown_cnt
    # Backup the origin file.

    # convert file from the source encoding to target encoding
    content = codecs.open(filename, 'rb').read()
    source_encoding = chardet.detect(content)['encoding']
    total_cnt += 1
    if source_encoding == None:
        print_pro("??{}".format(filename), constants.WARN_PRINT)
        unkown_cnt += 1
        return
    print("  ", source_encoding, filename)
    if source_encoding != 'utf-8' and source_encoding != 'UTF-8-SIG':
        # .encode(source_encoding)
        content = content.decode(source_encoding, 'ignore')
        codecs.open(filename, 'w', encoding='UTF-8-SIG').write(content)
    success_cnt += 1


def convert_dir(root_dir):
    if os.path.exists(root_dir) == False:
        print_pro("[error] DIR: {} do not exit".format(
            root_dir), constants.ERROR_PRINT)
    print("work in", root_dir)
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if check_need_convert(f):
                filename = os.path.join(root, f)
                try:
                    convert_encoding_to_utf_8(filename)
                except Exception as e:
                    print("WA", filename, e)
    print_pro("finish total: {}, success: {}, unkown_cnt: {}".format(
        total_cnt, success_cnt, unkown_cnt))
