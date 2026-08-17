import os
import multiprocessing
import argparse
import json
from hdf5filewriter import HDF5FileWriter
from lerobotfilewriter import LeRobotFileWriter
from datetime import datetime

def isValidFolderName(name:str)->bool:
    try:
        datetime.strptime(name, '%Y%m%d%H%M%S')
        return True
    except:
        return False
 
# **************************************************************************************************   
def parseHdf5(configs):
    #configs是一个数组，每个元素的配置具体可以参考HDF5FileWriter类的说明
    count = len(configs)
    for idx, cfg in enumerate(configs):
        episode = cfg["record_name"]
        print(f"Processing dataset {episode}", flush=True)
        hdf5 = HDF5FileWriter()
        hdf5.process_dataset(cfg)
        print(f"Processing dataset {episode} finished: {idx+1}/{count}", flush=True)
    print(f"hdf5 file has process finished", flush=True)

# ************************************************************************************************** 
def parseLeRobot(config):
    #config是一个对象，配置具体可以参考LeRobotFileWriter类的说明
    lerobot = LeRobotFileWriter()
    lerobot.process_dataset(config)
    print(f"lerobot file has process finished", flush=True)

# **************************************************************************************************
def formatFile(strFileJson):
    with open(strFileJson, 'r', encoding='utf-8') as file:
        data = json.load(file)
    fmt = data["format"] # 转换的格式
    configs = data["config"] #各种配置信息
    if fmt == "hdf5":
        parseHdf5(configs)
    elif fmt == "lerobot":
        parseLeRobot(configs)
    else:
        print(f"不支持的文件格式{fmt}", flush=True)

'''
请使用 pyinstaller --name robotformatapp main.py 方式打包
'''
####
if __name__  == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-file", "--file", help="json配置文件绝对路径")
        args,unknown = parser.parse_known_args() # args = parser.parse_args()
        multiprocessing.freeze_support()
        formatFile(args.file)
    except Exception as e:
        print(f"格式化导出文件出现错误: {e}", flush=True)
