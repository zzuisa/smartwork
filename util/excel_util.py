from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Alignment
import os
import copy
import time


__all__ = ['open_file', 'open_or_add_sheet', 'data_excel', 'export_to_excel']

# 批量插入支持传入'A1' 和 [row,col]形式的数据
# 批量插入数据
# mode 0 横向 1 纵向


def batch_insert(ws, _list, pos=[1, 1], mode=0):
    row, column = 1, 1
    if isinstance(pos, str):
        row, column = [ord(str(pos[0:1]).upper())-65+1, int(pos[1:])]
    if isinstance(pos, list):
        row, column = pos
    if mode == 0:
        for index, value in enumerate(_list):
            ws.cell(row=row, column=column+index,
                    value=value).alignment = Alignment(horizontal='center', vertical='center')
            # 居中处理
    else:
        for index, value in enumerate(_list):
            ws.cell(row=row+index, column=column,
                    value=value).alignment = Alignment(horizontal='center', vertical='center')
    return ws


def open_file(excel_name_path):
    return Workbook() if not os.path.isfile(excel_name_path) else load_workbook(str(excel_name_path))

# 检查是否存在当前sheet_name, 若不存在则新建并以此命名第一个sheet


def open_or_add_sheet(workbook, sheet_name):
    worksheet = workbook.active
    if sheet_name in workbook.sheetnames:
        worksheet = workbook[sheet_name]
    else:
        worksheet = workbook.create_sheet(sheet_name)
        del workbook[workbook.sheetnames[0]]
    return worksheet

# 执行插入数据
def data_excel(excel_name_path, workbook, worksheet, title, data):
    datain = copy.copy(data)  # 浅拷贝
    if isinstance(datain, dict):
        _, values = zip(*datain.items())
    if isinstance(datain, list):
        values = datain
    value_normal = values
    worksheet = batch_insert(worksheet, title, [1, 1])
    for index, value in enumerate(value_normal):
        worksheet = batch_insert(worksheet, value, [2+index, 1])
    b = workbook.save(excel_name_path)
    workbook.close()
    return worksheet

# 主函数
def export_to_excel(path, title, data, sheet_name='Default'):
    wb = open_file(path)
    ws = open_or_add_sheet(wb, sheet_name)
    data_excel(path, wb, ws, title, data)
