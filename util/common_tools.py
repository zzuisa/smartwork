# -*- encoding: utf-8 -*-
'''
@文件        :common_tools.py
@说明        :
@时间        :2022/09/28 16:25:38
@作者        :awx1192780
@版本        :1.0
'''

from base import constants
from datetime import datetime
import os
import sys


def print_pro(text, p_type=constants.SUCCESS_PRINT, sub=''):
    """
    高亮输出
    @param text: 要输出的文本1
    @param sub: 要输出的文本2, 以标准格式输出  
    @param p_type: 输出类别 'success' 'info' 'error' 'warn'
    """
    
    if p_type == constants.SUCCESS_PRINT:
        print('\033[2;32;40m{}\033[0m{}'.format(text, sub))
    elif p_type == constants.ERROR_PRINT:
        print('\n\n\n\033[2;31;40m{}\033[0m{}'.format(text, sub))
        sys.exit(1)
    elif p_type == constants.WARN_PRINT:
        print('\033[2;33;40m{}\033[0m{}'.format(text, sub))

def get_cur_folder_name():
    '''
    获取当日工作目录名称，如: 20221021周五    
    '''
    return '{}{}'.format(datetime.now().strftime('%Y%m%d'), ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()])