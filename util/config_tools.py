# -*- encoding: utf-8 -*-
'''
@文件        :config_tools.py
@说明        :
@时间        :2022/09/28 15:30:16
@作者        :awx1192780
@版本        :1.0
'''


import configparser
import sys


class Config:

    @staticmethod
    def reader(instance_name=None):
        config = configparser.ConfigParser()
        config.read('./confs/conf.ini', encoding='utf-8')
        instance_config = {}
        if instance_name:
            try:
                instance_config = dict(config[instance_name])
                return instance_config
            except:
                print('不存在此配置项！')
                return sys.exit()
        return config