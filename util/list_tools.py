# -*- encoding: utf-8 -*-
'''
@文件        :list_util.py
@说明        :
@时间        :2022/10/04 10:26:11
@作者        :awx1192780
@版本        :1.0
'''


__all__ = ['one_layer']

def one_layer(_list):
    """
    只保留1层list
    @param 待处理的list类型的数据
    @return list
    """
    if len(_list) == 0:
        return _list
    if isinstance(_list[0],list):
        return one_layer(_list[0])
    return _list