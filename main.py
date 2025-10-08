# -*- encoding: utf-8 -*-
'''
@文件        :main.py
@说明        :优化版本 - 提升整体性能
@时间        :2022/09/15 10:26:50
@作者        :awx1192780
@版本        :1.1 - 性能优化版本
'''
import sys
import time
import re
from functools import lru_cache
from base import constants
from handler.file_handler import keys_list, traverse
from crontab.auto import create_daily_work_folder
from util.excel_tools import to_count_excel, to_report_excel

@lru_cache(maxsize=1)
def get_current_timestamp():
    """缓存当前时间戳"""
    return time.strftime('%Y%m%d%H%M%S', time.localtime())


def parse_arguments():
    """解析命令行参数 - 优化版本"""
    before_date = None
    simple_mode = False
    dates = None
    infos = ''
    
    if len(sys.argv) == 2 and sys.argv[1] == 'auto':
        return 'auto', before_date, simple_mode, dates, infos
    
    # 预编译正则表达式
    date_pattern = re.compile(r'^\d+$')
    
    if len(sys.argv) == 2 and date_pattern.match(str(sys.argv[1])):
        before_date = f'{time.localtime().tm_year}{sys.argv[1]}'
    
    if '-s' in sys.argv:
        simple_mode = True
    
    # 优化参数解析
    for arg in sys.argv[1:]:
        if ',' in arg:
            dates = arg
            n_dates = dates.replace(',', '-')
            infos = f'[{n_dates}]'
            break
    
    return 'process', before_date, simple_mode, dates, infos


if __name__ == '__main__':
    t = get_current_timestamp()
    mode, before_date, simple_mode, dates, infos = parse_arguments()
    
    if mode == 'auto':
        create_daily_work_folder()
    else:
        # 使用优化的文件处理
        smart_dict, res_dict = traverse(before_date, dates)
        
        # spec_column 代表[根因分析]列的列标，设置后，会自动根据行数调整单元格宽高。
        template_path = f'{constants.TEMPLATE_FOLDER}/{constants.TEMPLATE_SHEET_NAME}.xlsx'
        
        to_report_excel(
            res_dict, 
            infos=infos, 
            template_path=template_path,
            template_sheet_name=constants.TEMPLATE_SHEET_NAME, 
            spec_column="I", 
            simple_mode=simple_mode
        )
        
        # 统计功能已注释，如需要可取消注释
        # to_count_excel(
        #     smart_dict, 
        #     template_path=template_path,
        #     template_sheet_name=constants.TEMPLATE_SHEET_NAME, 
        #     infos=infos
        # )