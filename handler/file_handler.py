# -*- encoding: utf-8 -*-
'''
@文件        :file_handler.py
@说明        :
@时间        :2022/10/21 11:57:58
@作者        :awx1192780
@版本        :1.0
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
from tqdm import tqdm
from base import constants
from util.common_tools import print_pro
from util.config_tools import Config
from util.encoding_converter_tools import convert_dir

config = Config.reader()
smartwork_config = Config.reader('smartwork')
third_party = str(smartwork_config["third_party"])
non_problem = str(smartwork_config["non_problem"])
system_config = str(smartwork_config["system_config"])
system = str(smartwork_config["system"])
bussiness_config = str(smartwork_config["bussiness_config"])
transfer_to_requirement = str(smartwork_config["transfer_to_requirement"])
consultation = str(smartwork_config["consultation"])
version_update = str(smartwork_config["version_update"])
gray_upgrade_deployment = str(smartwork_config["gray_upgrade_deployment"])
alarm_monitoring_inspection = str(
    smartwork_config["alarm_monitoring_inspection"])
faq = str(smartwork_config["faq"])
version_update_meeting = str(smartwork_config["version_update_meeting"])
resource_management = str(smartwork_config["resource_management"])

keys_list = [third_party, non_problem, system_config, system, bussiness_config, transfer_to_requirement, consultation,
             version_update, gray_upgrade_deployment, alarm_monitoring_inspection, faq, version_update_meeting, resource_management]
ISSUES = dict(config['issue-types'])
DEFAULT_SOLVED_TIME = 2
DEFAULT_SOLVED_STATUS = 'Closed'
DEFAULT_SOLVED_COUNTRY = 'SG'
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
    _file = open(path, 'r', encoding='utf-8')

    # 检索当前工作日志
    def verify(keys_list, line):
        # 遍历Header
        for i in keys_list:
            if retrieve_name(i)[0] not in smart_dict:
                smart_dict[retrieve_name(i)[0]] = 0
            if re.sub(r'【(.*)】', r'\1', i) == line.split('#')[0]:
                return retrieve_name(i)[0]
    # 生成交付件
    _re = '.*工作日报(\d+).txt'
    cur_date = re.search(_re, path).group(1)
    cur_date = '{}/{}/{}'.format(cur_date[:4], cur_date[4:6], cur_date[6:8])
    if_record = False
    _contents = []
    descs = []
    print(_file.name)
    lines = _file.readlines()
    _len = len(lines)
    _report_dict = {}
    _cur_title = ''
    for _index, line in enumerate(lines):
        _list = []
        # 问题分类#外部单号#业务系统#应用模块#问题大类
        filtered_str = re.sub(
            r'.*【([\w、]*)-?(\w*)】【(\w{2,3})[:：]?([\w\s?]*)\[?(\w*)-?(\w*)\]?】(.*)', r'\1#\2#\3#\4#\5#\6#\7', line).strip()
        filtered_list = filtered_str.split('#')
        comment = re.search(r'^\*\*[\s]*(.*)', line.strip())
        res = verify(keys_list, filtered_str)
        if len(descs) != 0 and _cur_title != '':
            _report_dict[_cur_title][8] = '{}'.format('\n'.join(descs))
        _content = re.sub(r'\d\.?(.*】)?(.*\w)[\.:：。]?', r'\2', line).strip()
        type_group = re.search('【(.*)】', line)

        if len(filtered_list) == 7 and filtered_list[6] == '':
            continue
        # 判断当前读取的行不是1. 2. 等空行
        if re.sub('\d{1,2}\.', '', line).strip() != '':
            # TODO 这里有个bug： 如果当前行是第一行，且含有 1. 【关键词】则取出来的数据的头部会带有一个类似' '的字符，但这个并不是普通的空格或是tab，
            # 也不是全角的空格（无法使用strip()过滤），具体是什么，目前不清楚，但是就是会占位2个单位长度(str)，只有10月之后会有这个情况，推测是因为
            # 10月之后的日志文件变为GBK，而GBK转UTF-8 过程中，有为转换的字符导致的。
            # 暂时先这样处理：
            if _index == 0 and ' ' != line[:1]:
                line = line[2:]
            # 判断当前读取的行是否是标题行。
            if re.match('\s?\d{1,2}\.', line) != None and type_group != None and (len(filtered_list) == 7 and filtered_list[6] != ''):
                _type = type_group.group(1)
                # print('type',_type)

                _cur_title = uuid.uuid1()
                # filtered_list： 问题分类 外部单号 国家 业务系统 应用模块 问题大类 问题描述
                # ["外部单号","业务系统","应用模块","问题发现时间","问题处理时长","状态","问题分类","问题描述","根因分析","国家","责任人","备注","问题大类"]
                _report_dict[_cur_title] = [filtered_list[1].strip(),
                                            filtered_list[3].strip(),
                                            filtered_list[4].strip(),
                                            cur_date,
                                            DEFAULT_SOLVED_TIME,
                                            DEFAULT_SOLVED_STATUS,
                                            filtered_list[0].strip(),
                                            re.sub(
                    r'(\w*)[\.:：。\?？]?', r'\1', filtered_list[5]).strip(),
                    '',
                    constants.COUNTRY_MAP[filtered_list[2].upper(
                    )],
                    DEFAULT_SOLVED_OWNER,
                    '',
                    ISSUES[str(filtered_list[5]).lower()]]
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
                    _report_dict[_cur_title][11] += comment.group(
                        1).replace('- ', '')
                if if_record and _index != _len-1 and not line.strip().startswith('**'):
                    descs.append(
                        re.sub('【.*】', '', line.replace('\t', '').replace('- ', '').strip()))
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
            # 扫描文件夹，对文件夹内相关的文件进行编码检查、转码等
            convert_dir(dirpath)
            for report in os.listdir(dirpath):
                if '.txt' in report:
                    file_path = '{}\\{}'.format(
                        dirpath, report).replace('\\', '\\\\')
                    smart_dict, res_dict = do_count(
                        smart_dict, res_dict, file_path)
    return smart_dict, res_dict
