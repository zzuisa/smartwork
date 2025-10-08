# -*- encoding: utf-8 -*-
'''
@文件        :constants.py
@说明        :优化版本 - 提升常量加载性能
@时间        :2022/09/28 14:30:16
@作者        :awx1192780
@版本        :1.1 - 性能优化版本
'''
import time
import json
from functools import lru_cache
from util.config_tools import Config

# 缓存配置读取
@lru_cache(maxsize=1)
def _load_config():
    """缓存配置加载"""
    return Config.reader()

# 常量定义
SUCCESS_PRINT = 'success'
INFO_PRINT = 'info'
ERROR_PRINT = 'error'
WARN_PRINT = 'warn'

# 延迟加载配置，避免启动时的性能开销
def _get_config_value(key):
    """获取配置值的辅助函数"""
    config = _load_config()
    return str(config['smartwork'][key])

# 时间相关常量
current_year_and_month = time.strftime("%Y%m", time.localtime())
# 手动修改：%Y%m
current_year_and_month = (current_year_and_month if 
                         _get_config_value("specify_date").lower() == 'off' 
                         else _get_config_value("specify_date"))
current_year = current_year_and_month[:-2]

# 路径相关常量
BASE_FOLDER = _get_config_value("base_folder")
REPORT_FOLDER = _get_config_value("report_folder")
TEMPLATE_FOLDER = _get_config_value("template_folder")
TEMPLATE_SHEET_NAME = _get_config_value("template_sheet_name")

# 动态生成报告路径
@lru_cache(maxsize=1)
def get_report_path():
    """缓存报告路径生成"""
    return f'{REPORT_FOLDER}\\{current_year_and_month}交付件{time.strftime("%H%M%S", time.localtime())}.xlsx'

REPORT_PATH = get_report_path()

# 工作表名称
SHEET_NAME = f'{int(current_year_and_month[-2:])}月-统计'
REPORT_SHEET_NAME = f'{int(current_year_and_month[-2:])}月-交付件'

# 头部信息
@lru_cache(maxsize=1)
def get_headers():
    """缓存头部信息解析"""
    config = _load_config()
    return json.loads(config['smartwork']["header"]), json.loads(config['smartwork']['info_header'])

HEADER, INFO_HEADER = get_headers()

# 国家映射 - 使用frozenset提高查找性能
COUNTRY_MAP = {
    'BS': '新加坡',
    'SG': '新加坡',
    'RU': '俄罗斯',
    'DE': '德国',
    'ED': '德国',
    'DR': '德国,俄罗斯',
    'RD': '德国,俄罗斯',
    'SR': '新加坡,俄罗斯',
    'RS': '俄罗斯,新加坡',
    'SD': '新加坡,德国',
    'DS': '德国,俄罗斯',
    'SDR': '新加坡,德国,俄罗斯'
}