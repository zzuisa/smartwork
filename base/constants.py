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

# 国家映射 - 从配置文件读取，不使用缓存保持原始大小写
def get_country_map():
    """获取国家映射配置，不使用缓存保持原始大小写"""
    config = _load_config()
    country_mapping = config['country-mapping']
    return {k.upper(): v for k, v in country_mapping.items()}

COUNTRY_MAP = get_country_map()

# 默认值配置 - 从配置文件读取
@lru_cache(maxsize=1)
def get_default_values():
    """缓存默认值配置"""
    config = _load_config()
    return {
        'solved_time': int(config['smartwork']['default_solved_time']),
        'solved_status': config['smartwork']['default_solved_status'],
        'solved_country': config['smartwork']['default_solved_country'],
        'solved_owner': config['smartwork']['default_solved_owner'],
        'region': config['smartwork']['default_region']
    }

DEFAULT_VALUES = get_default_values()

# 文件处理配置
@lru_cache(maxsize=1)
def get_file_config():
    """缓存文件处理配置"""
    config = _load_config()
    return {
        'encoding': config['smartwork']['file_encoding'],
        'supported_types': eval(config['smartwork']['supported_file_types']),
        'batch_size': int(config['smartwork']['batch_size']),
        'cache_size': int(config['smartwork']['cache_size'])
    }

FILE_CONFIG = get_file_config()

# Excel配置
@lru_cache(maxsize=1)
def get_excel_config():
    """缓存Excel配置"""
    config = _load_config()
    return {
        'default_width': float(config['smartwork']['excel_default_width']),
        'max_width': float(config['smartwork']['excel_max_width']),
        'row_height': int(config['smartwork']['excel_row_height']),
        'header_height': int(config['smartwork']['excel_header_height']),
        'spec_column_width': int(config['smartwork']['excel_spec_column_width']),
        'prev_column_width': int(config['smartwork']['excel_prev_column_width'])
    }

EXCEL_CONFIG = get_excel_config()

# 性能配置
@lru_cache(maxsize=1)
def get_performance_config():
    """缓存性能配置"""
    config = _load_config()
    return {
        'enable_caching': config['performance']['enable_caching'].lower() == 'true',
        'cache_max_size': int(config['performance']['cache_max_size']),
        'enable_progress_bar': config['performance']['enable_progress_bar'].lower() == 'true',
        'enable_monitoring': config['performance']['enable_performance_monitoring'].lower() == 'true',
        'batch_size': int(config['performance']['batch_processing_size']),
        'memory_optimization': config['performance']['memory_optimization'].lower() == 'true'
    }

PERFORMANCE_CONFIG = get_performance_config()

# 正则表达式模式配置
@lru_cache(maxsize=1)
def get_regex_patterns():
    """缓存正则表达式模式"""
    config = _load_config()
    return {
        'work_report': config['regex-patterns']['work_report_pattern'],
        'filter_str': config['regex-patterns']['filter_str_pattern'],
        'comment': config['regex-patterns']['comment_pattern'],
        'type_group': config['regex-patterns']['type_group_pattern'],
        'numbered_line': config['regex-patterns']['numbered_line_pattern'],
        'clean_desc': config['regex-patterns']['clean_desc_pattern'],
        'bracket_clean': config['regex-patterns']['bracket_clean_pattern']
    }

REGEX_PATTERNS = get_regex_patterns()

# 时间配置
@lru_cache(maxsize=1)
def get_time_config():
    """缓存时间配置"""
    config = _load_config()
    return {
        'default_hours': int(config['time-config']['default_work_hours']),
        'case_output_hours': int(config['time-config']['case_output_hours']),
        'base_auto_hours': int(config['time-config']['base_auto_hours']),
        'gray_upgrade_hours': int(config['time-config']['gray_upgrade_hours']),
        'it_query_hours': int(config['time-config']['it_query_hours']),
        'business_consultation_hours': int(config['time-config']['business_consultation_hours']),
        'alarm_hours': int(config['time-config']['alarm_hours']),
        'change_implementation_hours': int(config['time-config']['change_implementation_hours'])
    }

TIME_CONFIG = get_time_config()