import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(current_dir)+'/lerobot')

import dataclasses
from pathlib import Path
import cv2
from typing import Literal
from lerobot.lerobot_dataset_v21 import LeRobotDataset
import numpy as np
import tqdm
import shutil
import glob
import pickle
import json
import jsonlines


@dataclasses.dataclass(frozen=True)
class DatasetConfig:
    use_videos: bool = True
    tolerance_s: float = 0.0001
    image_writer_processes: int = 10
    image_writer_threads: int = 5
    video_backend: None = None


DEFAULT_DATASET_CONFIG = DatasetConfig()


def create_empty_dataset(
        root_dir: str,
        repo_id: str,
        robot_type: str,
        mode: Literal["video", "image"] = "video",
        *,
        dataset_config: DatasetConfig = DEFAULT_DATASET_CONFIG,
) -> LeRobotDataset:
    """创建空的lerobot格式数据"""
    motors = [
        "arm_left_J1",
        "arm_left_J2",
        "arm_left_J3",
        "arm_left_J4",
        "arm_left_J5",
        "arm_left_J6",
        "arm_left_J7",
        "hand_left_J1",
        "hand_left_J2",
        "hand_left_J3",
        "hand_left_J4",
        "hand_left_J5",
        "hand_left_J6",
        "arm_right_J1",
        "arm_right_J2",
        "arm_right_J3",
        "arm_right_J4",
        "arm_right_J5",
        "arm_right_J6",
        "arm_right_J7",
        "hand_right_J1",
        "hand_right_J2",
        "hand_right_J3",
        "hand_right_J4",
        "hand_right_J5",
        "hand_right_J6",
        "head_J1",
        "head_J2",
    ]
    cameras = [
        "cam_high_left",
        "cam_high_right",
        "cam_left_wrist",
        "cam_right_wrist",
    ]

    features = {
        "observation.state": {
            "dtype": "float64",
            "shape": (len(motors),),
            "names": [
                motors,
            ],
        },
        "action": {
            "dtype": "float64",
            "shape": (len(motors),),
            "names": [
                motors,
            ],
        },
    }

    for cam in cameras:
        features[f"observation.images.{cam}"] = {
            "dtype": mode,
            # "shape": (3, 480, 640),
            "shape": (3, 224, 224),
            "names": [
                "channels",
                "height",
                "width",
            ],
        }
    return LeRobotDataset.create(
        root=root_dir,
        repo_id=repo_id,
        fps=50,
        robot_type=robot_type,
        features=features,
        use_videos=dataset_config.use_videos,
        tolerance_s=dataset_config.tolerance_s,
        image_writer_processes=dataset_config.image_writer_processes,
        image_writer_threads=dataset_config.image_writer_threads,
        video_backend=dataset_config.video_backend,
    )

def read_img(im):
    """读取并缩放图片"""
    im = cv2.imread(im)
    im = cv2.resize(im, (224, 224))
    return im

def get_image_list(im_path):
    """读取所有的JPG文件并且排序"""
    img_list = glob.glob(os.path.join(im_path, '*.jpg'))
    img_list.sort(key=lambda x: int(os.path.basename(x).split(".")[0]))
    return img_list

def load_annotation(file_path, len_step):
    """加载标注信息,每一帧的数据的任务标签，返回列表，长度为该回合帧数"""
     # 默认的任务名字
    annos_js = ["do the task"]*len_step  # 未标注的数据默认
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path) :
            with open(file_path, 'r', encoding='utf-8')as file:
                data=json.load(file)
        if int(data["state"])==1:   # 标注后的数据
            steps_config = data["steps"]
            for task in steps_config:
                task_min = task["min"]
                task_max = task["max"]+1
                annos_js[task_min:task_max]=[task["text"]]*(task_max-task_min)
    except Exception as e:
        pass
    return annos_js

def load_data(one_dataset_dir):
    """加载单个文件夹里面的数据"""
    data_pose_list = glob.glob(os.path.join(one_dataset_dir, 'observation', '*.pkl'))
    data_pose_list.sort(key=lambda x: int(os.path.basename(x).split(".")[0]))
    cam_high_left_list = get_image_list(os.path.join(one_dataset_dir, 'top_left'))
    cam_high_right_list = get_image_list(os.path.join(one_dataset_dir, 'top_right'))
    cam_left_wrist_list = get_image_list(os.path.join(one_dataset_dir, 'wrist_left'))
    cam_right_wrist_list = get_image_list(os.path.join(one_dataset_dir, 'wrist_right'))
    
    qpos = []
    action = []
    imgs_per_cam = {}
    image_li = [[], [], [], []]
    for i in range(len(data_pose_list)):
        with open(data_pose_list[i], "rb") as f:
            data_single = pickle.load(f)
            qpos.append(data_single['obs'])
            action.append(data_single['action'])
            image_li[0].append(read_img(cam_high_left_list[i]))
            image_li[1].append(read_img(cam_high_right_list[i]))
            image_li[2].append(read_img(cam_left_wrist_list[i]))
            image_li[3].append(read_img(cam_right_wrist_list[i]))

    annos_info_list = load_annotation(os.path.join(one_dataset_dir, "annotationcfg", "config.json"), len(qpos))

    imgs_per_cam['cam_high_left'] = np.array(image_li[0])
    imgs_per_cam['cam_high_right'] = np.array(image_li[1])
    imgs_per_cam['cam_left_wrist'] = np.array(image_li[2])
    imgs_per_cam['cam_right_wrist'] = np.array(image_li[3])
    return imgs_per_cam, np.array(qpos), np.array(action), annos_info_list


def populate_dataset(dataset: LeRobotDataset,
                     list_files: None = None,
                     episodes: None = None) -> LeRobotDataset:
    """转换原始数据到lerobot格式"""
    if episodes is None:
        episodes = range(len(list_files))

    for ep_idx in tqdm.tqdm(episodes):
        ep_path = list_files[ep_idx]
        imgs_per_cam, state, action, task_name_l = load_data(ep_path)
        num_frames = state.shape[0]
        # add prompt
        for i in range(num_frames):
            frame = {
                "observation.state": state[i],
                "action": action[i],
                "task": task_name_l[i]
            }

            for camera, img_array in imgs_per_cam.items():
                tmp_img_arr = img_array[i][:, :, ::-1].swapaxes(0, 2).swapaxes(1, 2)
                frame[f"observation.images.{camera}"] = tmp_img_arr
            dataset.add_frame(frame)
        dataset.save_episode()
    return dataset




class LeRobotFileWriter:
    def __init(self):
        pass

    """
    # config数据结构建议是这样
    config = {
        "save_dir":"", # 转换成lerobot后保存的绝对路径 /home/test/savepath/train_data
        "all_record_dir":["","",""...] # 所有录制回合的文件夹，即带时间戳的文件夹: /home/test/taskname/collect_data/20250529112345
    }
    注意事项：
        1. save_dir目录必须不能存在，lerobot库自己检测到如果存在则会报错。
        2. save_dir目录可以允许多级不存在。lerobot库会逐级创建目录。
    """

    # 处理所有数据
    def process_dataset(self, config) -> None:
        raw_dataset_list = config["all_record_dir"]
        save_dir = config["save_dir"]

        # 如果路径存在，全部清除之后，重新生成数据
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        # 创建空的lerobot数据格式
        dataset_empty = create_empty_dataset(
            root_dir=save_dir,
            repo_id="",
            robot_type="atom",
            mode="image",
            dataset_config=DEFAULT_DATASET_CONFIG,
        )

        ## 写入数据
        dataset = populate_dataset(
            dataset=dataset_empty,
            list_files=raw_dataset_list
        )

'''
if __name__=="__main__":
        ## 遍历原始数据文件夹
    raw_dir = r"E:\lfworkspace\project\gitlab\DobotRX\x64_output\Debug\robotcollectdata\qqqa\collect_data"
    episodes = os.listdir(raw_dir)
    episodes.sort(key=lambda x: int(x))
    raw_dataset_list = [os.path.join(str(raw_dir), i) for i in episodes]
    print(raw_dataset_list)
    config = {"all_record_dir": raw_dataset_list, 
              "save_dir": r"E:\lfworkspace\project\gitlab\DobotRX\x64_output\Debug\robotcollectdata\qqqa\exportdata\大多数的\haoa"}
    test = LeRobotFileWriter()
    test.process_dataset(config)
'''