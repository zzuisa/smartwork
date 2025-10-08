# -*- encoding: utf-8 -*-
'''
@文件        :config_tools.py
@说明        :优化版本 - 提升配置读取性能
@时间        :2022/09/28 15:30:16
@作者        :awx1192780
@版本        :1.1 - 性能优化版本
'''

import configparser
import sys
from functools import lru_cache


class Config:
    _config_cache = None
    _config_file = './confs/conf.ini'

    @classmethod
    @lru_cache(maxsize=32)
    def reader(cls, instance_name=None):
        """
        配置读取器 - 优化版本，保持原始配置值
        @param instance_name: 与config.ini文件中的[section]对应
        @return 以dict的格式返回该section
        """
        # 使用类级别的缓存，避免重复读取配置文件
        if cls._config_cache is None:
            cls._config_cache = configparser.ConfigParser()
            # 保持原始大小写
            cls._config_cache.optionxform = str
            cls._config_cache.read(cls._config_file, encoding='utf-8')
        
        if instance_name:
            try:
                return dict(cls._config_cache[instance_name])
            except KeyError:
                print(f'不存在此配置项: {instance_name}')
                sys.exit(1)
        
        return cls._config_cache
    
    @classmethod
    def clear_cache(cls):
        """清除配置缓存，用于配置更新后重新加载"""
        cls._config_cache = None
        cls.reader.cache_clear()