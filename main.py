# -*- encoding: utf-8 -*-
'''
@文件        :main.py
@说明        :
@时间        :2022/09/15 10:26:50
@作者        :awx1192780
@版本        :1.0
'''
import sys
from base import constants
from handler.file_handler import keys_list, traverse
from crontab.auto import create_daily_work_folder
from util.excel_tools import to_count_excel, to_report_excel
import time


if __name__ == '__main__':
    t = time.strftime('%Y%m%d%H%M%S',time.localtime())
    if len(sys.argv) == 1:
        smart_dict, res_dict = traverse()
        # spec_column 代表[根因分析]列的列标，设置后，会自动根据行数调整单元格宽高。
        to_report_excel(res_dict, template_path='{}/{}.xlsx'.format(constants.TEMPLATE_FOLDER, constants.TEMPLATE_SHEET_NAME),
                        template_sheet_name=constants.TEMPLATE_SHEET_NAME, spec_column="I")
        to_count_excel(smart_dict, template_path='{}/{}.xlsx'.format(constants.TEMPLATE_FOLDER, constants.TEMPLATE_SHEET_NAME),
        template_sheet_name=constants.TEMPLATE_SHEET_NAME)

    elif sys.argv[1] == 'auto':
        create_daily_work_folder()