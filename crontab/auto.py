# -*- encoding: utf-8 -*-
'''
@文件        :auto.py
@说明        :
@时间        :2022/10/18 13:03:35
@作者        :awx1192780
@版本        :1.0
'''


import time
import json
import os
import sys
from util.config_tools import Config
from util.common_tools import get_cur_folder_name
from base import constants


def create_daily_work_folder():
    '''
    创建每日工作目录
    '''
    config = Config.reader()
    auto = Config.reader('auto')
    base = json.loads(auto['base'])
    cce = auto['cce']
    envs = json.loads(auto['env'])
    regions = json.loads(auto['region'])
    modules = json.loads(auto['module'])
    base_folder = config['smartwork']['base_folder']
    cur_folder = '{}//{}//{}'.format(base_folder,
                                     constants.current_year_and_month,
                                     get_cur_folder_name())
    pre_text = '1. 【资源管理】【SG:CBG Myhuawei[-op]】\n- \n2. 【告警、监控、巡检】【RU:CBG Myhuawei[eCommerce-op]】处理俄罗斯电商告警:\n- \n根因分析: \n3. 【告警、监控、巡检】【SG:CBG Myhuawei[-op]】例行巡检 - CBG官网、电商中台、华为论坛 \n- 输出巡检报告： de-inspection{}.xlsx\n** 无异常指标\n'.format( time.strftime('%Y%m%d', time.localtime()))
    report_name = '工作日报{}.txt'.format(
        time.strftime('%Y%m%d', time.localtime()))
    for i in base:
        os.makedirs('{}\\{}'.format(cur_folder, i), exist_ok=True)
    with open('{}//{}'.format(cur_folder, report_name), 'w', encoding='utf-8') as the_file:
        the_file.write(pre_text)
    for env in envs:
        for region in regions:
            for module in modules:
                os.makedirs('{}\\{}\\{}\\{}\\{}'.format(
                    cur_folder, cce, env, region, module), exist_ok=True)
