# -*- encoding: utf-8 -*-
'''
@文件        :encoding_converter_tools.py
@说明        :优化版本 - 提升编码转换性能
@时间        :2022/10/18 10:16:37
@作者        :awx1192780
@版本        :1.1 - 性能优化版本
'''

import codecs
import os
import sys
import shutil
import re
import chardet
from functools import lru_cache
from util.common_tools import print_pro
from base import constants

# 使用frozenset提高查找性能
convertfiletypes = frozenset([
    ".xml",
    ".lua", 
    ".csd",
    ".py",
    ".txt"
])


@lru_cache(maxsize=1024)
def check_need_convert(filename):
    """
    检查文件编码是否需要转换 - 缓存优化版本
    @param filename: 要检查的文件名称
    @return True or False
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(filetype) for filetype in convertfiletypes)


# 使用类来管理计数器，避免全局变量
class ConversionStats:
    def __init__(self):
        self.total_cnt = 0
        self.success_cnt = 0
        self.unknown_cnt = 0
    
    def reset(self):
        self.total_cnt = 0
        self.success_cnt = 0
        self.unknown_cnt = 0

# 全局统计实例
stats = ConversionStats()


def convert_encoding_to_utf_8(filename):
    """
    将文件编码格式转为UTF-8 - 性能优化版本
    @param filename: 要检查的文件名称
    """
    global stats
    
    try:
        # 使用更高效的文件读取方式
        with open(filename, 'rb') as f:
            content = f.read()
        
        source_encoding = chardet.detect(content)['encoding']
        stats.total_cnt += 1
        
        if source_encoding is None:
            print_pro(f"?? {filename}", constants.WARN_PRINT)
            stats.unknown_cnt += 1
            return
        
        if source_encoding not in ('utf-8', 'UTF-8-SIG'):
            content = content.decode(source_encoding, 'ignore')
            with open(filename, 'w', encoding='UTF-8-SIG') as f:
                f.write(content)
        
        stats.success_cnt += 1
        
    except Exception as e:
        print_pro(f"转换文件失败: {filename}, 错误: {e}", constants.ERROR_PRINT)


def convert_dir(root_dir):
    """
    待转换编码的文件目录 - 性能优化版本
    @param root_dir: 要检查的文件目录
    """
    if not os.path.exists(root_dir):
        print_pro(f"[error] DIR: {root_dir} do not exist", constants.ERROR_PRINT)
        return
    
    # 批量收集需要转换的文件，减少重复的路径操作
    files_to_convert = []
    try:
        for root, dirs, files in os.walk(root_dir):
            for f in files:
                if check_need_convert(f):
                    files_to_convert.append(os.path.join(root, f))
    except (OSError, PermissionError) as e:
        print_pro(f"遍历目录失败: {root_dir}, 错误: {e}", constants.ERROR_PRINT)
        return
    
    # 批量处理文件转换
    for filename in files_to_convert:
        try:
            convert_encoding_to_utf_8(filename)
        except Exception as e:
            print_pro(f"转换文件失败: {filename}, 错误: {e}", constants.WARN_PRINT)
    
    # 可选：输出统计信息
    # print_pro(f"finish total: {stats.total_cnt}, success: {stats.success_cnt}, unknown_cnt: {stats.unknown_cnt}")
