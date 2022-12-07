# -*- encoding: utf-8 -*-
'''
@文件        :constants.py
@说明        :
@时间        :2022/09/28 14:30:16
@作者        :awx1192780
@版本        :1.0
'''
import time
import json
from util.config_tools import Config

config = Config.reader()
SUCCESS_PRINT = 'success'
INFO_PRINT = 'info'
ERROR_PRINT = 'error'
WARN_PRINT = 'warn'
current_year_and_month = time.strftime("%Y%m", time.localtime())
# 手动修改：%Y%m
current_year_and_month = current_year_and_month if str(
    config['smartwork']["specify_date"]).lower() == 'off' else str(config['smartwork']["specify_date"])
#####
current_year = current_year_and_month[:-2]
BASE_FOLDER = str(config['smartwork']["base_folder"])
REPORT_FOLDER = str(config['smartwork']["report_folder"])
TEMPLATE_FOLDER = str(config['smartwork']["template_folder"])
TEMPLATE_SHEET_NAME = str(config['smartwork']["template_sheet_name"])
REPORT_PATH = '{}\\{}交付件{}.xlsx'.format(REPORT_FOLDER, current_year_and_month, time.strftime('%d%H%M%S',time.localtime()))
# 导出的文件名
SHEET_NAME = '{}月-统计'.format(int(current_year_and_month[-2:]))
REPORT_SHEET_NAME = '{}月-交付件'.format(int(current_year_and_month[-2:]))
HEADER = json.loads(config['smartwork']["header"])
INFO_HEADER = json.loads(config['smartwork']['info_header'])

COUNTRY_MAP = {
    'BS' : '新加坡',
    'SG' : '新加坡',
    'RU' : '俄罗斯',
    'DE' : '德电',
    'ED' : '德电',
    'DR' : '德电、俄罗斯',
    'RD' : '德电、俄罗斯',
    'SR' : '新加坡、俄罗斯',
    'RS' : '俄罗斯、新加坡',
    'SD' : '新加坡、德电',
    'DS' : '德电、俄罗斯',
    'SDR': '新加坡、德电、俄罗斯'
}