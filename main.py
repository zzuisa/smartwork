# -*- encoding: utf-8 -*-
'''
@文件        :main.py
@说明        :
@时间        :2022/09/15 10:26:50
@作者        :awx1192780
@版本        :1.0
'''


import os
import time
import glob
import json
import configparser
import inspect
import collections
import re
import pandas as pd
import openpyxl
from openpyxl import Workbook
from tqdm import tqdm
from util.excel_util import export_to_excel
from util.list_util import one_layer

config = configparser.ConfigParser()
config.read('./confs/conf.ini', encoding='UTF-8')
current_year_and_month = time.strftime("%Y%m", time.localtime())
# 手动修改：
current_year_and_month = "202209"
#####
current_year = current_year_and_month[:-2]
EVENT = str(config['smartwork']["event"])
TROUBLESHOOTING = str(config['smartwork']["troubleshooting"])
PM = str(config['smartwork']["pm"])
ALARM = str(config['smartwork']["alarm"])
VERSION_UPDATE = str(config['smartwork']["version_update"])
VERSION_UPDATE_MEETING = str(config['smartwork']["version_update_meeting"])
ACTIVE_OPERATION_MAINTAIN = str(
    config['smartwork']["active_operation_maintain"])
FAQ = str(config['smartwork']["faq"])
NEGATIVE_EVENT = str(config['smartwork']["negative_event"])
BASE_FOLDER = str(config['smartwork']["base_folder"])
REPORT_FOLDER = str(config['smartwork']["report_folder"])
REPORT_PATH = '{}\\{}交付件.xlsx'.format(REPORT_FOLDER, current_year)
SHEET_NAME = '{}月'.format(int(current_year_and_month[-2:]))
REPORT_SHEET_NAME = '{}月-交付件'.format(int(current_year_and_month[-2:]))
HEADER = json.loads(config['smartwork']["header"])
INFO_HEADER = json.loads(config['smartwork']['info_header'])
keys_list = [EVENT, TROUBLESHOOTING, PM, ALARM, VERSION_UPDATE,
             VERSION_UPDATE_MEETING, ACTIVE_OPERATION_MAINTAIN, FAQ, NEGATIVE_EVENT]


# 检索全局变量
def retrieve_name(var):
    return [var_name for var_name, var_val in inspect.currentframe().f_globals.items() if var_val == var]


def copy_dict_from(source_dict: dict):
    target_dict = collections.defaultdict(int)
    if isinstance(source_dict, dict):
        for i in source_dict.keys():
            target_dict[i] = 0
    return target_dict

# 统计数量


def do_count(smart_dict, report_dict, path):
    if '.txt' not in path:
        return None
    _file = open(path, 'r', encoding='UTF-8')

    # 检索当前工作日志
    def verify(keys_list, line):
        for i in keys_list:
            if retrieve_name(i)[0] not in smart_dict:
                smart_dict[retrieve_name(i)[0]] = 0
            if line.find(i) != -1:
                return retrieve_name(i)[0]
    # 生成交付件
    _re = '.*工作日报(\d+).txt'
    cur_date = re.search(_re, path).group(1)
    cur_date = '{}/{}/{}'.format(cur_date[:4], cur_date[4:6], cur_date[6:8])
    if_record = False
    _contents = []
    descs = []
    lines = _file.readlines()
    _len = len(lines)
    _report_dict = {}
    for _index, line in enumerate(lines):
        _list = []
        res = verify(keys_list, line)
        _content = re.sub(r'\d\.?(.*】)?(.*\w)[\.:：。]?', r'\2', line).strip()
        type_group = re.search('【(.*)】', line)
        if re.sub('\d{1,2}\.', '', line).strip() != '':
            if re.match('\s?\d{1,2}\.', line) != None and type_group != None:
                _type = type_group.group(1)
                _report_dict[_content] = [_type, cur_date, 2]
                # 记录当前内容
                if_record = True
                if len(descs) != 0:
                    _contents.append(descs)
                descs = []
            elif re.match('\s?\d{1,2}\.', line) != None and type_group == None:
                # 不记录当前内容
                if_record = False
                if len(descs) != 0:
                    _contents.append(descs)
                descs = []
            else:
                if if_record and _index != _len-1:
                    descs.append(
                        re.sub('【.*】', '', line.replace('\t', '').replace('- ', "◊ ")))
            if res:
                smart_dict[res] += 1
    if len(descs) != 0:
        _contents.append(descs)
    if len(_contents) < len(_report_dict):
        _contents.extend([[] for i in range(len(_report_dict)-len(_contents))])
    for _index, item in enumerate(_report_dict):
        _report_dict[item].append('{}'.format(''.join(_contents[_index])))
    for k, v in _report_dict.items():
        v.insert(0, k)
    report_dict = {**report_dict, **_report_dict}
    _contents = []
    # print('report',report_dict)
    return smart_dict, report_dict


# 导出Excel


def to_excel(smart_dict):
    try:
        df = pd.DataFrame([smart_dict.values()], columns=[
                          i.replace('【', '').replace('】', '') for i in keys_list])
        processed_data = df.values.tolist()
        if os.path.exists(REPORT_FOLDER) == False:
            os.makedirs(REPORT_FOLDER)
        print('[processed_data] {} TO {}  => [{}]'.format(json.dumps(dict(zip(HEADER, one_layer(
            processed_data))), indent=4, ensure_ascii=False), str(REPORT_PATH), SHEET_NAME))
        export_to_excel(str(REPORT_PATH), HEADER, processed_data, SHEET_NAME, data_type='count')
    except Exception as e:
        print("导出失败，不存在目录或文件正在被使用。", e)

def to_report_excel(report_dict, spec_column):
    try:
            df = pd.DataFrame(list(report_dict.values()), columns=[INFO_HEADER])
            processed_data = df.values.tolist()
            if os.path.exists(REPORT_FOLDER) == False:
                os.makedirs(REPORT_FOLDER)
            print('[report_data] {} TO {} => [{}]'.format(json.dumps(dict(zip(INFO_HEADER, one_layer(
                processed_data))), indent=4, ensure_ascii=False), str(REPORT_PATH), REPORT_SHEET_NAME))
            export_to_excel(str(REPORT_PATH), INFO_HEADER,
                            processed_data, REPORT_SHEET_NAME, 'report', spec_column)
    except Exception as e:
        print("导出失败，不存在目录或文件正在被使用。", e)
# 文件夹检索


def traverse():
    smart_dict = collections.defaultdict(int)
    res_dict = {}
    if os.path.exists(BASE_FOLDER) == False:
        print('不存在此目录:{}'.format(BASE_FOLDER))
        os._exit(0)
    for dirname in tqdm(os.listdir(BASE_FOLDER), desc='输出报告', position=0):
        dirpath = '{}\\{}'.format(BASE_FOLDER, dirname)
        if current_year_and_month in dirname and os.path.isdir(dirpath):
            for report in os.listdir(dirpath):
                if '.txt' in report:
                    file_path = '{}\\{}'.format(
                        dirpath, report).replace('\\', '\\\\')
                    smart_dict, res_dict = do_count(
                        smart_dict, res_dict, file_path)
    return smart_dict, res_dict


if __name__ == '__main__':
    smart_dict, res_dict = traverse()
    to_excel(smart_dict)
    to_report_excel(res_dict,spec_column="E")
