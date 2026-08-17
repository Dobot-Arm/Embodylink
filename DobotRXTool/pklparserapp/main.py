import os
import argparse
import glob
import pickle
import json
import numpy as np

def convert_to_serializable(obj):
    """将不可序列化的对象转换为可序列化的格式，只考虑这几种格式"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    else:
        return obj

def parsePklFile(dir, begIdx, endIdx):
    try:
        jsoncachePath = os.path.join(dir,'cache')
        if not os.path.exists(jsoncachePath):
            os.makedirs(jsoncachePath)
        #allfiles = glob.glob(os.path.join(dir,'*.pkl'))
        for i in range(begIdx, endIdx+1):
            file_names = f"{i}.pkl"
            filepath = os.path.join(dir,file_names)
            try:
                # 读取pkl文件
                with open(filepath, 'rb') as pkl_file:
                    data = pickle.load(pkl_file)
            
                # 处理数据使其可以序列化
                if isinstance(data, dict):
                    converted_data = {k: convert_to_serializable(v) for k, v in data.items()}
                elif isinstance(data, list):
                    converted_data = [convert_to_serializable(item) for item in data]
                else:
                    converted_data = convert_to_serializable(data)

                # 写入json文件
                with open(os.path.join(jsoncachePath,file_names+'.json'), 'w', encoding='utf-8') as json_file:
                    json.dump(converted_data, json_file, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"转换过程中出现错误: {e}")
    except Exception as e:
        print(f"遍历过程中出现错误: {e}")

'''
请使用 pyinstaller --name pklparserapp main.py 方式打包
'''
####
if __name__  == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--dir", help="pkl文件夹路径")
    parser.add_argument("-begin", "--begin", type=int, help="pkl文件开始序号")
    parser.add_argument("-end", "--end", type=int, help="pkl文件结束序号")
    args = parser.parse_args()
    parsePklFile(args.dir, args.begin, args.end)