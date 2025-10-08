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
    ms = json.loads(auto['ms'])
    base_folder = config['smartwork']['base_folder']
    cur_year = time.strftime("%Y", time.localtime())
    cur_folder = '{}//{}//{}//{}'.format(base_folder,
                                         cur_year,
                                     constants.current_year_and_month,
                                     get_cur_folder_name())
    pre_text = '1. 【案例输出】【DE:vmall[vmall-op]】\n \n2. 【IT数据查询】【DE:vmall[vmall-op]】\n\n3. 【业务咨询问题】【DE:vmall[vmall-cons]】\n\n3. 【业务咨询问题】【SG:CBG Myhuawei[CMCC-cons]】\n\n4.【告警、监控、巡检】【DE:vmall[vmall-op]】\n \n5.【灰度升级部署】【DE:vmall[vmall-op]】\n\n5.【灰度升级部署】【DE:CBG Myhuawei[海外论坛-op]】\n\n6.【变更评审】【DE:vmall[vmall-op]】\n\n6.【变更评审】【DE:CBG Myhuawei[海外论坛-op]】\n\n7.【变更实施-】【DE:vmall[vmall-op]】\n\n8.【资源管理-】【DE:vmall[vmall-op]】\n\n'.format( time.strftime('%Y%m%d', time.localtime()))
    report_name = '工作日报{}.txt'.format(
        time.strftime('%Y%m%d', time.localtime()))
    for i in base:
        os.makedirs('{}\\{}'.format(cur_folder, i), exist_ok=True)
    with open('{}//{}'.format(cur_folder, report_name), 'w', encoding='utf-8') as the_file:
        the_file.write(pre_text)
    for env in envs:
        for region in regions:
            for s in ms:
                os.makedirs('{}\\{}\\{}\\{}\\{}'.format(
                    cur_folder, cce, env, region, s), exist_ok=True)

    """
    第三方问题		非华为系统异常造成的华为系统异常，华为内部系统异常属于系统配置问题/系统问题
系统配置问题		需要更改it配置才能修复的问题，要有dts单
系统问题			系统gbug，需要
转需求			当前it系统不支持此功能，需要安排需求上线，要确认和业务握手成功才能选择此分类
变更实施			版本变更/sp变更/运维优化变更
灰度升级部署		灰度升级
告警、监控、巡检	告警处理等
案例输出			要写明输出的地址以及标题
变更评审			要给出明确结论，通过/不通过以及原因
资源管理			删机器，调整规格，删资源，关小黑屋，买机器等
业务咨询问题		业务找到对应责任人进行功能咨询、业务逻辑咨询
业务配置问题		业务配置错误导致现网有影响，包括但不限于价格、描述、展示方式等等
安全事件			日常安全攻击事件等
漏洞治理			主机打补丁，cce升级等等
合规类			产品合规改造，合规审计等，不要写个人的考试
IT数据查询		开发找过来查数据，查配置，查各种
运维优化			其他各种运维的问题

overseas_classification	Third party	第三方问题	consulting	
overseas_classification	sys conf	系统配置问题	configuration	
overseas_classification	sys bug	系统问题	BUG	
overseas_classification	to requirement	转需求	consulting	
overseas_classification	change execute	变更实施	operate	
overseas_classification	gray	灰度升级部署	operate	
overseas_classification	monitor	告警、监控、巡检	operate	
overseas_classification	issue	案例输出	operate	
overseas_classification	change review	变更评审	operate	
overseas_classification	resource manage	资源管理	operate	
overseas_classification	ops optimization	运维优化	operate	
overseas_classification	business conf	业务配置问题	data	
overseas_classification	securityIssue	安全事件	security	
overseas_classification	vulnerability_governance	漏洞治理	security	
overseas_classification	compiance	合规类	security	
overseas_classification	IT data query	IT数据查询	operate	
overseas_classification	business consulting	业务咨询问题	consulting

    """