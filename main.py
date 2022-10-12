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
from tqdm import tqdm
from base import constants
from util.common_tools import print_pro
from util.excel_tools import to_excel, to_report_excel
from util.config_tools import Config

config = Config.reader()
smartwork_config = Config.reader('smartwork')
EVENT = str(smartwork_config["event"])
TROUBLESHOOTING = str(smartwork_config["troubleshooting"])
PM = str(smartwork_config["pm"])
ALARM = str(smartwork_config["alarm"])
VERSION_UPDATE = str(smartwork_config["version_update"])
VERSION_UPDATE_MEETING = str(smartwork_config["version_update_meeting"])
ACTIVE_OPERATION_MAINTAIN = str(
    smartwork_config["active_operation_maintain"])
FAQ = str(smartwork_config["faq"])
NEGATIVE_EVENT = str(smartwork_config["negative_event"])
keys_list = [EVENT, TROUBLESHOOTING, PM, ALARM, VERSION_UPDATE,
             VERSION_UPDATE_MEETING, ACTIVE_OPERATION_MAINTAIN, FAQ, NEGATIVE_EVENT]
ISSUES = dict(config['issue-types'])
DEFAULT_SOLVED_TIME = 2
DEFAULT_SOLVED_STATUS = 'Closed'
DEFAULT_SOLVED_COUNTRY = '新加坡'
DEFAULT_SOLVED_OWNER = '孙奥'
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
        # 遍历Header
        for i in keys_list:
            if retrieve_name(i)[0] not in smart_dict:
                smart_dict[retrieve_name(i)[0]] = 0
            if line.find(re.sub(r'【(.*)】', r'\1', i)) != -1:
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
    _cur_title = ''
    for _index, line in enumerate(lines):
        _list = []
        # 问题分类#外部单号#业务系统#应用模块#问题大类
        filtered_str = re.sub(
            r'.*【([\w、]*)-?(\w*)】【BS[:：]?([\w\s?]*)\[?(\w*)-?(\w*)\]?】(.*)', r'\1#\2#\3#\4#\5#\6', line).strip()
        filtered_list = filtered_str.split('#')
        comment = re.search(r'^\*\*[\s]*(.*)', line.strip())
        res = verify(keys_list, filtered_str)
        if len(descs) != 0 and _cur_title != '':
            _report_dict[_cur_title][8] = '{}'.format('\n'.join(descs))
        _content = re.sub(r'\d\.?(.*】)?(.*\w)[\.:：。]?', r'\2', line).strip()
        type_group = re.search('【(.*)】', line)
        if len(filtered_list) == 6 and filtered_list[5] == '':
            continue
        # 判断当前读取的行不是1. 2. 等空行
        if re.sub('\d{1,2}\.', '', line).strip() != '':
            # 判断当前读取的行是否是标题行。
            if re.match('\s?\d{1,2}\.', line) != None and type_group != None and (len(filtered_list) == 6 and filtered_list[5] != ''):
                _type = type_group.group(1)
                _cur_title = _content
                # ["外部单号","业务系统","应用模块","问题发现时间","问题处理时长","状态","问题分类","问题描述","根因分析","国家","责任人","备注","问题大类"]
                _report_dict[_content] = [filtered_list[1],
                                          filtered_list[2],
                                          filtered_list[3],
                                          cur_date,
                                          DEFAULT_SOLVED_TIME,
                                          DEFAULT_SOLVED_STATUS,
                                          filtered_list[0],
                                          re.sub(
                                              r'(\w*)[\.:：。\?？]?', r'\1', filtered_list[5]),
                                          '',
                                          DEFAULT_SOLVED_COUNTRY,
                                          DEFAULT_SOLVED_OWNER,
                                          '',
                                          ISSUES[str(filtered_list[4]).lower()]]
                # 记录当前内容
                if_record = True

                descs = []
            elif re.match('\s?\d{1,2}\.', line) != None and type_group == None:
                # 如果是 1. xxxx 的形式，不记录当前内容
                if_record = False
                if len(descs) != 0:
                    _report_dict[_cur_title][8] = '{}'.format('\n'.join(descs))
                descs = []
            else:
                if comment and _cur_title != '':
                    _report_dict[_cur_title][11] += comment.group(1)
                if if_record and _index != _len-1 and not line.strip().startswith('**'):
                    descs.append(
                        re.sub('【.*】', '', line.replace('\t', '').replace('- ', "").strip()))
            if res:
                smart_dict[res] += 1
    if len(descs) != 0:
        _report_dict[_cur_title][8] = '{}'.format('\n'.join(descs))

    report_dict = {**report_dict, **_report_dict}
    _contents = []
    return smart_dict, report_dict


# 文件夹检索


def traverse():
    smart_dict = collections.defaultdict(int)
    res_dict = {}
    if os.path.exists(constants.BASE_FOLDER) == False:
        print('不存在此目录:{}'.format(constants.BASE_FOLDER))
        os._exit(0)
    for dirname in tqdm(os.listdir(constants.BASE_FOLDER), desc='输出报告', position=0):
        dirpath = '{}\\{}'.format(constants.BASE_FOLDER, dirname)
        if constants.current_year_and_month in dirname and os.path.isdir(dirpath):
            for report in os.listdir(dirpath):
                if '.txt' in report:
                    file_path = '{}\\{}'.format(
                        dirpath, report).replace('\\', '\\\\')
                    smart_dict, res_dict = do_count(
                        smart_dict, res_dict, file_path)
    return smart_dict, res_dict


if __name__ == '__main__':
    smart_dict, res_dict = traverse()
    # to_excel(smart_dict, template_path='{}/{}.xlsx'.format(TEMPLATE_FOLDER, TEMPLATE_SHEET_NAME),
    #  template_sheet_name=TEMPLATE_SHEET_NAME,)
    # spec_column 代表[根因分析]列的列标，设置后，会自动根据行数调整单元格宽高。
    to_report_excel(res_dict, template_path='{}/{}.xlsx'.format(constants.TEMPLATE_FOLDER, constants.TEMPLATE_SHEET_NAME),
                    template_sheet_name=constants.TEMPLATE_SHEET_NAME, spec_column="I")
