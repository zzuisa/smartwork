# -*- encoding: utf-8 -*-
'''
@文件        :file_handler.py
@说明        :优化版本 - 提升文件处理性能
@时间        :2022/10/21 11:57:58
@作者        :awx1192780
@版本        :1.1 - 性能优化版本
'''
import os
import sys
import time
import glob
import json
import configparser
import inspect
import collections
import uuid
import re
from functools import lru_cache
from tqdm import tqdm
from base import constants
from util.common_tools import print_pro
from util.config_tools import Config
from util.encoding_converter_tools import convert_dir

# 缓存配置读取，避免重复解析
@lru_cache(maxsize=1)
def _get_cached_config():
    """缓存配置读取"""
    config = Config.reader()
    smartwork_config = Config.reader('smartwork')
    return config, smartwork_config

# 预编译正则表达式，避免重复编译
class RegexCache:
    def __init__(self):
        self._cache = {}
    
    def get_pattern(self, pattern):
        if pattern not in self._cache:
            self._cache[pattern] = re.compile(pattern)
        return self._cache[pattern]

# 全局正则表达式缓存
regex_cache = RegexCache()

# 预编译常用正则表达式 - 从配置文件读取
@lru_cache(maxsize=1)
def get_patterns():
    """从配置文件获取正则表达式模式"""
    patterns = {}
    for key, pattern in constants.REGEX_PATTERNS.items():
        patterns[key] = regex_cache.get_pattern(pattern)
    return patterns

PATTERNS = get_patterns()

# 缓存配置数据
config, smartwork_config = _get_cached_config()

# 预计算配置值，避免重复字符串转换
CONFIG_VALUES = {
    'third_party': str(smartwork_config["third_party"]),
    'non_problem': str(smartwork_config["non_problem"]),
    'system_config': str(smartwork_config["system_config"]),
    'system': str(smartwork_config["system"]),
    'bussiness_config': str(smartwork_config["bussiness_config"]),
    'transfer_to_requirement': str(smartwork_config["transfer_to_requirement"]),
    'consultation': str(smartwork_config["consultation"]),
    'version_update': str(smartwork_config["version_update"]),
    'gray_upgrade_deployment': str(smartwork_config["gray_upgrade_deployment"]),
    'alarm_monitoring_inspection': str(smartwork_config["alarm_monitoring_inspection"]),
    'faq': str(smartwork_config["faq"]),
    'version_update_meeting': str(smartwork_config["version_update_meeting"]),
    'resource_management': str(smartwork_config["resource_management"]),
    'compliant': str(smartwork_config["compliant"]),
    'security_issue': str(smartwork_config["security_issue"]),
    'it_consulation': str(smartwork_config["it_consulation"])
}

keys_list = list(CONFIG_VALUES.values())
ISSUES = dict(config['issue-types'])

# 使用配置文件中的默认值
DEFAULT_SOLVED_TIME = constants.DEFAULT_VALUES['solved_time']
DEFAULT_SOLVED_STATUS = constants.DEFAULT_VALUES['solved_status']
DEFAULT_SOLVED_COUNTRY = constants.DEFAULT_VALUES['solved_country']
DEFAULT_SOLVED_OWNER = constants.DEFAULT_VALUES['solved_owner']
DEFAULT_REGION = constants.DEFAULT_VALUES['region']

# 预计算键名映射，避免重复inspect调用
@lru_cache(maxsize=32)
def get_key_name(value):
    """缓存键名查找"""
    return [var_name for var_name, var_val in CONFIG_VALUES.items() if var_val == value]


def retrieve_name(var):
    """保持向后兼容，但使用缓存版本"""
    return get_key_name(var)


def copy_dict_from(source_dict: dict):
    """优化字典复制，使用更高效的方式"""
    if isinstance(source_dict, dict):
        return collections.defaultdict(int, {k: 0 for k in source_dict.keys()})
    return collections.defaultdict(int)


def do_count(smart_dict, report_dict, path):
    """
    统计数量 - 性能优化版本
    @param path: 报告所在工作目录
    """
    if '.txt' not in path:
        return None
    
    # 使用with语句确保文件正确关闭
    with open(path, 'r', encoding='utf-8') as _file:
        # 检索当前工作日志 - 优化版本
        def verify(keys_list, line):
            # 使用预编译的正则表达式
            clean_line = PATTERNS['bracket_clean'].sub('', line.split('#')[0])
            for i in keys_list:
                key_name = get_key_name(i)[0] if get_key_name(i) else None
                if key_name and key_name not in smart_dict:
                    smart_dict[key_name] = 0
                if PATTERNS['bracket_clean'].sub('', i) == clean_line:
                    return key_name
            return None
        
        # 生成交付件 - 使用预编译正则表达式
        match = PATTERNS['work_report'].search(path)
        if not match:
            return None
            
        cur_date = match.group(1)
        cur_date = f'{cur_date[:4]}-{cur_date[4:6]}-{cur_date[6:8]}'
        
        if_record = False
        descs = []
        lines = _file.readlines()
        lines.append('\n')
        _len = len(lines)
        _report_dict = {}
        _cur_title = ''
        
        for _index, line in enumerate(lines):
            # 问题分类#外部单号#业务系统#应用模块#问题大类
            filtered_str = PATTERNS['filter_str'].sub(r'\1#\2#\3#\4#\5#\6#\7', line).strip()
            filtered_list = filtered_str.split('#')
            comment = PATTERNS['comment'].search(line.strip())
            res = verify(keys_list, filtered_str)
            
            if len(descs) != 0 and _cur_title != '':
                _report_dict[_cur_title][8] = '\n'.join(descs)
            
            type_group = PATTERNS['type_group'].search(line)
            
            if len(filtered_list) == 7 and filtered_list[6] == '':
                if_record = False
                continue
            
            # 判断当前读取的行不是1. 2. 等空行
            if PATTERNS['numbered_line'].sub('', line).strip() != '':
                if (PATTERNS['numbered_line'].match(line) is not None and 
                    type_group is not None and len(filtered_list) == 7):
                    
                    _cur_title = uuid.uuid1()
                    # filtered_list： 问题分类 外部单号 国家 业务系统 应用模块 问题大类 问题描述
                    # ["外部单号","业务系统","应用模块","问题发现时间","问题处理时长","状态","问题分类","问题描述","根因分析","国家","区域","责任人","备注","问题大类"]
                    _report_dict[_cur_title] = [
                        filtered_list[1].strip(),
                        filtered_list[3].strip(),
                        filtered_list[4].strip(),
                        cur_date,
                        generate_time(filtered_list),
                        DEFAULT_SOLVED_STATUS,
                        filtered_list[0].strip(),
                        PATTERNS['clean_desc'].sub(r'\1', filtered_list[6]).strip(),
                        '',
                        check_origin(filtered_list),
                        DEFAULT_REGION,
                        DEFAULT_SOLVED_OWNER,
                        '',
                        ISSUES[str(filtered_list[5]).lower()]
                    ]
                    if_record = True
                    descs = []
                    
                elif (PATTERNS['numbered_line'].match(line) is not None and 
                      type_group is None):
                    # 如果是 1. xxxx 的形式，不记录当前内容
                    if_record = False
                    if len(descs) != 0:
                        _report_dict[_cur_title][8] = '\n'.join(descs)
                    descs = []
                else:
                    if comment and _cur_title != '':
                        _report_dict[_cur_title][12] += comment.group(1).replace('- ', '')
                    if if_record and _index != _len-1 and not line.strip().startswith('**'):
                        descs.append(
                            PATTERNS['bracket_clean'].sub('', 
                                line.replace('\t', '').replace('- ', '').strip()))
            
            if res:
                smart_dict[res] += 1
        
        if len(descs) != 0 and _cur_title != '':
            _report_dict[_cur_title][8] = '\n'.join(descs)
        
        # 使用更高效的字典合并
        report_dict.update(_report_dict)
        return smart_dict, report_dict

def generate_time(filtered_list):
    """
    生成工作时长 - 从配置文件读取
    @param filtered_list: 通过正则过滤后的列表 
    """
    q_type = filtered_list[0]
    q_desc = filtered_list[6]
    time_config = constants.TIME_CONFIG
    
    if '案例输出' in q_type:
        if 'sg-auto' in q_desc:
            return time_config['base_auto_hours']
        return time_config['case_output_hours']
    if '灰度升级部署' in q_type:
        return time_config['gray_upgrade_hours']
    if 'IT数据查询' in q_type:
        return time_config['it_query_hours']
    if '业务咨询问题' in q_type:
        return time_config['business_consultation_hours']
    if '告警' in q_type:
        return time_config['alarm_hours']
    if '变更实施' in q_type:
        return time_config['change_implementation_hours']
    
    return time_config['default_hours']
def check_origin(filtered_list):
    country_map = constants.COUNTRY_MAP
    if filtered_list[2].upper() != 'SG':
        return country_map[filtered_list[2].upper()]
    for country_name in set(country_map.values()):
        if country_name in filtered_list[6]:
            return country_name
    return country_map[filtered_list[2].upper()]


def traverse(before_date=None, dates=None):
    """
    文件夹检索 - 性能优化版本
    @param before_date: 由main函数传进来的参数，表示检索before_date日期(含)之后的报告 
    """
    smart_dict = collections.defaultdict(int)
    res_dict = {}
    root_path = os.path.join(constants.BASE_FOLDER, constants.current_year, constants.current_year_and_month)
    
    if not os.path.exists(constants.BASE_FOLDER):
        print(f'不存在此目录:{constants.BASE_FOLDER}')
        os._exit(0)
    
    # 预计算时间戳，避免重复计算
    before_timestamp = None
    start_timestamp = None
    end_timestamp = None
    
    if before_date:
        before_timestamp = time.mktime(time.strptime(before_date, '%Y%m%d'))
    
    if dates:
        start, end = dates.split(',')
        start_timestamp = time.mktime(time.strptime(f'{constants.current_year_and_month}{start}', "%Y%m%d"))
        end_timestamp = time.mktime(time.strptime(f'{constants.current_year_and_month}{end}', "%Y%m%d"))
    
    # 使用os.scandir()替代os.listdir()，性能更好
    try:
        with os.scandir(root_path) as entries:
            # 过滤并排序目录，减少不必要的处理
            dirs = [entry for entry in entries if entry.is_dir() and constants.current_year_and_month in entry.name]
            dirs.sort(key=lambda x: x.name)  # 按名称排序，确保处理顺序一致
            
            for entry in tqdm(dirs, desc='输出报告', position=0):
                dirname = entry.name
                dirpath = entry.path
                
                # 时间过滤优化
                try:
                    cur = time.mktime(time.strptime(dirname[:-2], '%Y%m%d'))
                    
                    if before_timestamp and cur < before_timestamp:
                        continue
                    if start_timestamp and end_timestamp and (cur < start_timestamp or cur > end_timestamp):
                        continue
                        
                except ValueError:
                    # 如果日期解析失败，跳过该目录
                    continue
                
                # 批量处理文件，减少重复的编码转换
                txt_files = []
                try:
                    with os.scandir(dirpath) as dir_entries:
                        txt_files = [f.path for f in dir_entries if f.is_file() and f.name.endswith('.txt')]
                except (OSError, PermissionError):
                    continue
                
                if txt_files:
                    # 只对包含txt文件的目录进行编码转换
                    convert_dir(dirpath)
                    
                    # 批量处理txt文件
                    for file_path in txt_files:
                        result = do_count(smart_dict, res_dict, file_path)
                        if result:
                            smart_dict, res_dict = result
                            
    except (OSError, PermissionError) as e:
        print(f'访问目录失败: {root_path}, 错误: {e}')
        return smart_dict, res_dict
    
    return smart_dict, res_dict
