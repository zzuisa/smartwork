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


def indicator_format(indicator_type, _list):
    """
    根据不同指标自定义格式化内容
    
    @param indicator_type: 资源类别
    @param _list: 要处理的源数据，list类型
    @return 格式化之后的数据  
    """
    
    if str(indicator_type).lower() == constants.RES_ELB:
        return ['{} Mbit/s'.format(str(round(i/1024/1024, 2))) if _index in [2] else i for _index, i in enumerate(_list)]
    elif str(indicator_type).lower() == constants.RES_NGINX:
        _list = ['{}%'.format(str(round(i, 2))) if _index in [
            0] else i for _index, i in enumerate(_list)]
        _list.insert(1, 'N/A')
        return _list
    elif str(indicator_type).lower() == constants.RES_CCE:
        return ['{}%'.format(str(round(i, 2))) if _index in [0, 1] else i for _index, i in enumerate(_list)]
    elif str(indicator_type).lower() == constants.RES_MYSQL:
        return ['{}%'.format(str(round(i, 2))) if _index in [0, 1] else i for _index, i in enumerate(_list)]
    elif str(indicator_type).lower() == constants.RES_REDIS:
        return ['{}%'.format(str(round(i, 2))) if _index in [1] else i for _index, i in enumerate(_list)]
    return _list


def get_cur_folder_name():
    '''
    获取当日工作目录名称，如: 20221021周五    
    '''
    return '{}{}'.format(datetime.now().strftime('%Y%m%d'), ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()])