import os, time, glob, json
import configparser
import inspect
import collections
import pandas as pd
import openpyxl
from openpyxl import Workbook
from tqdm import tqdm
from util.excel_util import export_to_excel
from util.list_util import one_layer

'''
基于工作日志导出月底交付件报表V.1.0
awx1192780
2022/09/15

[smartwork]
header = ["事件","故障","PM","告警","变更","变更评审","主动运维","FAQ","负向事件"]
base_folder = D:\\workspace
report_folder = D:\workspace\交付件
event = 【事件】
troubleshooting = 【故障】
pm = 【PM】
alarm = 【告警】
version_update = 【变更】
version_update_meeting = 【变更评审】
active_operation_maintain = 【主动运维】
faq = 【FAQ】
negative_event = 【负向事件】

'''
config = configparser.ConfigParser()
config.read('./confs/conf.ini',encoding='UTF-8')
current_year_and_month = time.strftime("%Y%m",time.localtime())
current_year = time.strftime("%Y",time.localtime())
EVENT = str(config['smartwork']["event"])
TROUBLESHOOTING = str(config['smartwork']["troubleshooting"])
PM = str(config['smartwork']["pm"])
ALARM = str(config['smartwork']["alarm"])
VERSION_UPDATE = str(config['smartwork']["version_update"])
VERSION_UPDATE_MEETING = str(config['smartwork']["version_update_meeting"])
ACTIVE_OPERATION_MAINTAIN = str(config['smartwork']["active_operation_maintain"])
FAQ = str(config['smartwork']["faq"])
NEGATIVE_EVENT = str(config['smartwork']["negative_event"])
BASE_FOLDER = str(config['smartwork']["base_folder"])
REPORT_FOLDER = str(config['smartwork']["report_folder"])
REPORT_PATH = '{}\\{}交付件.xlsx'.format(REPORT_FOLDER,current_year)
SHEET_NAME='{}月'.format(int(time.strftime('%m',time.localtime())))
HEADER = json.loads(config['smartwork']["header"])
keys_list = [EVENT,TROUBLESHOOTING,PM,ALARM,VERSION_UPDATE,VERSION_UPDATE_MEETING,ACTIVE_OPERATION_MAINTAIN,FAQ,NEGATIVE_EVENT]

# 检索全局变量
def retrieve_name(var):
    return [var_name for var_name, var_val in inspect.currentframe().f_globals.items() if var_val == var]

def copy_dict_from(source_dict:dict):
    target_dict = collections.defaultdict(int)
    if(isinstance(source_dict, dict)):
        for i in source_dict.keys():
            target_dict[i] = 0
    return target_dict

# 统计
def do_count(smart_dict,path):
    if('.txt' not in path):
        return None
    file = open(path,'r',encoding='UTF-8')
    def verify(keys_list,line):
        for i in keys_list:
            if(retrieve_name(i)[0] not in smart_dict):
                smart_dict[retrieve_name(i)[0]] = 0
            if line.find(i) != -1:
                return retrieve_name(i)[0]
    for line in file:
        res = verify(keys_list, line)
        if res:
            smart_dict[res] +=1
    return smart_dict

# 导出Excel
def to_excel(smart_dict):
    try:
        df = pd.DataFrame([smart_dict.values()], columns=[i.replace('【','').replace('】','') for i in keys_list])
        processed_data = df.values.tolist() 
        if os.path.exists(REPORT_FOLDER) == False:
            os.makedirs(REPORT_FOLDER)
        print('[processed_data] {} TO {}'.format(json.dumps(dict(zip(HEADER,one_layer(processed_data))),indent=4,ensure_ascii=False),str(REPORT_PATH)))
        export_to_excel(str(REPORT_PATH),HEADER,processed_data ,SHEET_NAME)
    except Exception as e:
        print("导出失败，不存在目录或文件正在被使用。",e)

# 文件夹检索        
def traverse():
    smart_dict = collections.defaultdict(int)
    if os.path.exists(BASE_FOLDER) == False:
        print('不存在此目录:{}'.format(BASE_FOLDER))
        os._exit(0)
    for dirname in tqdm(os.listdir(BASE_FOLDER),desc='搜索中'):
        dirpath = '{}\\{}'.format(BASE_FOLDER,dirname)
        if current_year_and_month in dirname and os.path.isdir(dirpath):
            for report in os.listdir(dirpath):
                if('.txt' in report):
                    file_path = '{}\\{}'.format(dirpath,report).replace('\\', '\\\\')
                    smart_dict = do_count(smart_dict, file_path)
    return smart_dict
if __name__ == '__main__':
    smart_dict = traverse()
    to_excel(smart_dict)